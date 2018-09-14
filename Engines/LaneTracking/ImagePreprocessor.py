import numpy
import cv2
from Settings.CozmoSettings import Settings


class ImagePreprocessor:

    sign_recognition_cooldown = False

    def __init__(self):
        pass

    def pil_rgb_to_numpy_binary(self, pil_img):
        """
        Convert an rgb pil image to binary numpy array
        :param pil_img: A pil image
        :return: A numpy array with values 0 as black, 1 as white
        """
        # Convert pil image to numpy array
        rgb_img = self.pil_to_numpy(pil_img)

        # Tri-channel (rgb) to single channel (grey)
        rgb_img = rgb_img[:, :, 1]

        # Convert gray image to binary image
        bin_img = self.gray_to_binary(rgb_img)

        return bin_img

    def gray_to_binary(self, image):
        """
        Converts an image to a binary image
        :param image: Numpy array representation of the greyscale image
        :return: Numpy array of the binary image
        """

        # Convert image values to binary mask
        bw_image = image > Settings.image_binarization_threshold

        # Convert array into int array
        bw_image = numpy.array(bw_image, dtype=numpy.uint8)

        return bw_image

    def pil_to_numpy(self, image):
        """
        Convert a pil image to a numpy array
        :param image: A pil image
        :return: A numpy array
        """
        arr = numpy.array(image, dtype=numpy.uint8)
        return arr

    def calculate_number_of_signs(self, image):
        """
        Tracks all contours and process them to find signs
        :param image: image in binary form
        :return: amount of tracked signs
        """
        image = numpy.array(image, dtype=numpy.uint8) - 1

        start_row_1 = int(image.shape[0] / 3)
        row_height = int((image.shape[0] - start_row_1) / 3)
        end_row_1 = start_row_1 + row_height
        end_row_2 = end_row_1 + row_height                      # used to start the measurement

        # Get multidimensional array of conture informations
        contours = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        contour_allowed = False
        contour_counter = 0
        for contour in contours[1]:
            if Settings.min_pixel_sign < cv2.contourArea(contour) < Settings.max_pixel_sign:
                cv2.drawContours(image, [contour], 0, 128, 2)
                contour_counter += 1
                contour_allowed = self.contours_in_allowed_area(contour, contour_allowed, end_row_2)

        # Option to show tracked contours in extra window
        if Settings.show_contures_in_extra_window:
            cv2.imshow("with contours", image)

        # Refreshes the amount of found contours if they are in allowed area
        if contour_allowed:
            sign_count = contour_counter
        # Sets amount of signs to zero if contours aren`t in allowed area
        else:
            sign_count = 0

        return sign_count

    def contours_in_allowed_area(self, contour, contour_allowed, end_row_2):
        if contour[0][0][1] > end_row_2:
            contour_allowed = True
        return contour_allowed
