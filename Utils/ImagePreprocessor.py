import numpy
import cv2
from itertools import groupby
from Settings.CozmoSettings import Settings


class ImagePreprocessor:

    @staticmethod
    def crop_image(image, top, right, bottom=None, left=None):
        """
        Crops the image by the given offsets
        :param image: The input image that should be cropped
        :type image: Numpy array
        :param top: Amount of pixels cropped from the top
        :param right: Amount of pixels cropped from the right
        :param bottom: Amount of pixels cropped from the bottom
        :param left: Amount of pixels cropped from the left
        :return: Cropped image
        :rtype: Numpy array
        """
        h, w = image.shape
        if bottom is None:
            bottom = top
        if left is None:
            left = right
        return image[top:h - bottom, left:w - right]

    @staticmethod
    def pil_rgb_to_numpy_binary(pil_img):
        """
        Convert an rgb pil image to binary numpy array
        :param pil_img: A pil image
        :return: A numpy array with values 0 as black, 1 as white
        """
        # Convert pil image to numpy array
        rgb_img = ImagePreprocessor.pil_to_numpy(pil_img)

        # Tri-channel (rgb) to single channel (gray)
        gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY)

        # Convert gray image to binary image
        bin_img = ImagePreprocessor.gray_to_binary(gray_img)

        # Apply smoothing by using morphological operations
        return ImagePreprocessor.morphological_opening(bin_img)

    @staticmethod
    def gray_to_binary(image):
        """
        Converts an image to a binary image
        :param image: Numpy array representation of the greyscale image
        :return: Numpy array of the binary image
        """

        # Convert image values to binary mask
        img_mask = image > Settings.preprocessor_binarization_threshold

        # Convert mask to int array
        bin_img = numpy.array(img_mask, dtype=numpy.uint8)

        return bin_img

    @staticmethod
    def morphological_opening(image):
        """
        Expand black areas with morphological opening
        :param image: The image to morph
        :type image: Numpy array
        :return: The morphed image
        :rtype: Numpy array
        """
        kernel = numpy.ones((3, 3), numpy.uint8)

        ret = image.copy()
        ret = cv2.erode(ret, kernel)
        ret = cv2.dilate(ret, kernel)
        return ret

    @staticmethod
    def pil_to_numpy(image):
        """
        Convert a pil image to a numpy array
        :param image: A pil image
        :return: A numpy array
        """
        arr = numpy.array(image, dtype=numpy.uint8)
        return arr

    @staticmethod
    def find_contours(image):
        """
        Gets an array of contours, each as a vector of points.
        :param image: Image containing the contours to find
        :return:
        """
        # Invert the image
        inverted_img = 1 - image

        # Calculate all detected contours
        contours_raw = cv2.findContours(inverted_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Use array of contours only
        contours = contours_raw[1]

        return contours

    @staticmethod
    def extract_lane_shape(image, contours):
        """
        Cuts out the lane shape from the input image.
        :param image: Input image
        :type image: Binary numpy array
        :param contours: An array of vectors of points representing the contours found
        :return: The image which contains only the lane shape
        :rtype: Numpy array
        """

        # Create new array with the input image size and fills it with 1's
        masked_img = numpy.full(image.shape, 1, dtype=numpy.uint8)

        # Take the contour with the biggest area (the lane shape)
        if not contours:
            return masked_img

        # Calculate area of contour area
        biggest_contour_area = max(contours, key=cv2.contourArea)

        # Fill elements within biggest area with 1's
        cv2.drawContours(masked_img, [biggest_contour_area], 0, color=0, thickness=cv2.FILLED)

        return masked_img

    @staticmethod
    def run_length_encoding(data_array):
        """
        Encode an array with run length run_length_encoding
        :param data_array: Data to Encode
        :type data_array: Array
        :return: The encoded Data
        :rtype: Numpy array
        """
        return numpy.array([[len(list(group)), name] for name, group in groupby(data_array)])

    @staticmethod
    def cleanup_row_noise(raw_pattern_data, min_required_length=Settings.lane_pattern_min_width_threshold):
        """
        Remove pixel runs, which are too short to be valid
        :param raw_pattern_data: The RLE data
        :param min_required_length: The minimum required length of a run for it to be valid
        :return: The RLE data with the short runs removed
        :rtype: Numpy array
        """
        new_list = [[0, -1]]
        last_run_too_short = False

        for i in range(raw_pattern_data.shape[0]):

            run_length = raw_pattern_data[i, 0]
            run_color = raw_pattern_data[i, 1]

            def run_too_small(x):
                return x < min_required_length

            list_is_empty = new_list[0][1] == -1

            # Run is too small -> run is added to previous run
            if run_too_small(run_length):
                # Add run length to last valid run
                new_list[-1][0] += run_length
                last_run_too_short = True

            elif last_run_too_short:
                # If last valid run was same color add to it, otherwise create new run
                if new_list[-1][1] == run_color or list_is_empty:
                    new_list[-1][0] += run_length
                    # Set color, in case last run is still -1
                    new_list[-1][1] = run_color
                else:
                    new_list.append(raw_pattern_data[i])

                last_run_too_short = False

            # Run is okay, add run to new list as is
            else:
                if list_is_empty:
                    new_list[0] = raw_pattern_data[i]
                else:
                    new_list.append(raw_pattern_data[i])

        return numpy.array(new_list)

    @staticmethod
    def calculate_number_of_signs(display_img, contours):
        """
        Extracts signs from contours
        :param display_img: Image for display purposes
        :param contours: An array of vectors of points representing the contours found
        :return: amount of tracked signs
        """

        # Gets the y coordinate of one third of the image
        top_offset = int(display_img.shape[0] / 3)

        # Set the position of the trigger line
        y_trigger_line = Settings.trigger_line_position

        # Only contours are important that have a certain size. Also checks if the contour
        # is below the line of measurement
        contour_below_trigger = False
        contour_counter = 0
        for contour in contours:

            # If any point of the contour is above the lower third of the frame ignore it
            if (contour[:, 0, 1] < top_offset).any():
                continue

            if Settings.sign_min_pixel_count < cv2.contourArea(contour) < Settings.sign_max_pixel_count:
                # Draw contour for display
                if Settings.live_preview_show_signs:
                    cv2.drawContours(display_img, [contour], 0, color=(34, 126, 230), thickness=cv2.FILLED)

                contour_counter += 1

                # if any point of the contour is below the trigger line
                if numpy.array(contour[:, 0, 1] > y_trigger_line).any():
                    contour_below_trigger = True

        # Option to show tracked contours in extra window
        if Settings.live_preview_show_signs:
            # draws the line for visual purposes
            cv2.line(display_img, (0, y_trigger_line), (display_img.shape[1], y_trigger_line),
                     color=(43, 57, 192), thickness=1)

        # Updates the amount of found contours if they are in allowed area
        if contour_below_trigger:
            sign_count = contour_counter
        # Sets amount of signs to zero if contours aren't in allowed area
        else:
            sign_count = 0

        return sign_count
