import numpy
from PIL import Image
from cv2 import *
from Settings.CozmoSettings import Settings


class ImagePreprocessor:

    def __init__(self):
        pass

    def rgb_to_bw(self, img_gray):
        # Cast rgb image to numpy array
        img_gray = self.pil_to_numpyarray(img_gray)[:, :, 1]

        # Convert gray image to bw image
        img_bw = self.grey_to_bw(img_gray)

        return img_bw

    def grey_to_bw(self, image):
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

    def smoothing(self, image):
        smoothed_image = image.copy()
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        smoothed_image = cv2.erode(smoothed_image, kernel)
        smoothed_image = cv2.dilate(smoothed_image, kernel)
        smoothed_image = cv2.dilate(smoothed_image, kernel)
        smoothed_image = cv2.erode(smoothed_image, kernel)

        return smoothed_image

    def pil_to_numpyarray(self, image):
        arr = numpy.array(image, dtype=numpy.uint8)
        return arr

    def numpyarray_to_pil(self, image):
        img = Image.fromarray(numpy.uint8(image * 255))
        return img
