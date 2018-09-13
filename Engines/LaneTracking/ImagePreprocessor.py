import numpy
import cv2
from Settings.CozmoSettings import Settings


class ImagePreprocessor:

    kernel = numpy.ones((3, 3), numpy.uint8)

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

        # Tri-channel (rgb) to single channel (gray)
        gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY)

        # Convert gray image to binary image
        bin_img = self.gray_to_binary(gray_img)

        # Apply smoothing by using morphological operations
        return self.morphological_opening(bin_img)

    def gray_to_binary(self, image):
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

    def morphological_opening(self, image):
        """
        Expand black areas with morphological opening
        :param image: The image to morph
        :type image: Numpy array
        :return: The morphed image
        :rtype: Numpy array
        """
        ret = image.copy()
        ret = cv2.erode(ret, self.kernel)
        ret = cv2.dilate(ret, self.kernel)
        return ret

    def pil_to_numpy(self, image):
        """
        Convert a pil image to a numpy array
        :param image: A pil image
        :return: A numpy array
        """
        arr = numpy.array(image, dtype=numpy.uint8)
        return arr

    def extract_lane_shape(self, image):
        """
        Cuts out the lane shape from the input image.
        :param image: Input image
        :type image: Binary numpy array
        :return: The image which contains only the lane shape
        :rtype: Numpy array
        """
        # Invert the image
        inverted_img = 1 - image

        # Create new array with the input image size and fills it with 1's
        masked_img = numpy.full(inverted_img.shape, 1, dtype=numpy.uint8)

        # Grab all detected contours
        contours = cv2.findContours(inverted_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]

        # Take the contour with the biggest area (the lane shape)
        biggest_contour_area = max(contours, key = cv2.contourArea)

        # Fill elements within area with 1's
        cv2.drawContours(masked_img, [biggest_contour_area], 0, 0, -1)
        return masked_img
