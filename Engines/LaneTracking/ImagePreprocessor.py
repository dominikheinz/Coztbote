import numpy
from PIL import Image
from cv2 import *


class ImagePreprocessor:

    def __init__(self):
        pass

    def rgb_to_bw(self, img_gray):
        # Cast rgb image to numpy array
        img_gray = self.pil_to_numpyarray(img_gray)[:, :, 1]

        # Convert gray image to bw image
        img_bw = self.grey_to_bw(img_gray, 38)

        img_bw = self.smoothing(img_bw)

        return img_bw

    def grey_to_bw(self, image, threshold=60):
        """
        Converts an image to a binary image
        :param image: Numpy array representation of the greyscale image
        :param threshold: Maximum value which to be mapped to 0, all above will be mapped to 1
        :return: Numpy array of the binary image
        """

        bw_image = image > threshold
        bw_image = bw_image * 1
        return bw_image

    def smoothing(self, image):
        smoothed_image = numpy.array(image, dtype=numpy.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        smoothed_image = cv2.erode(smoothed_image, kernel)
        smoothed_image = cv2.dilate(smoothed_image, kernel)
        smoothed_image = cv2.dilate(smoothed_image, kernel)
        smoothed_image = cv2.erode(smoothed_image, kernel)

        return smoothed_image

    def pil_to_numpyarray(self, image):
        return numpy.array(image)

    def numpyarray_to_pil(self, image):
        return Image.fromarray(numpy.uint8(image * 255))
