import numpy
import cv2
from Settings.CozmoSettings import Settings
from itertools import groupby


class ImagePreprocessor:

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
        img_mask = image > Settings.image_binarization_threshold

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
    def extract_lane_shape(image):
        """
        Cuts out the lane shape from the input image.
        :param image: Input image
        :type image: Binary numpy array
        :return: The image which contains only the lane shape and an image containing only the lane surroundings
        :rtype: Numpy array, numpy array
        """

        # Invert the image
        inverted_img = 1 - image

        # Create new array with the input image size and fills it with 1's
        masked_img = numpy.full(inverted_img.shape, 1, dtype=numpy.uint8)

        # Grab all detected contours
        contours = cv2.findContours(
            inverted_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]

        # Take the contour with the biggest area (the lane shape)
        biggest_contour_area = max(contours, key=cv2.contourArea)

        # Fill elements within area with 1's
        cv2.drawContours(masked_img, [biggest_contour_area], 0, 0, -1)

        # Create a new image containing only the data surrounding the lane
        lane_surroundings_mask = numpy.zeros(inverted_img.shape, dtype=numpy.uint8)
        cv2.drawContours(lane_surroundings_mask, [biggest_contour_area], 0, 1, Settings.cozmo_lane_surrounding_width_px * 2)
        cv2.drawContours(lane_surroundings_mask, [biggest_contour_area], 0, 0, cv2.FILLED)

        # invert again to get the mainly white image back
        lane_surroundings = 1 - (inverted_img * lane_surroundings_mask)

        return masked_img, lane_surroundings

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

            def run_too_small(x): return x < min_required_length
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
