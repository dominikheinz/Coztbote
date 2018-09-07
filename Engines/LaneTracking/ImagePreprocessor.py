import numpy
from PIL import Image
from cv2 import *


class ImagePreprocessor:

    def __init__(self):
        pass

    def rgb_to_bw(self, img_rgb):

        # Cast rgb image to numpy array
        img_rgb = self.pil_to_numpyarray(img_rgb)

        # Convert to gray scale image
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

        # Convert gray image to bw image
        img_bw = self.grey_to_bw(img_gray)

        # Convert array to image
        return self.numpyarray_to_pil(img_bw)

    def grey_to_bw(self, image, threshold=127):
        '''
        Converts an image to a binary image
        :param image: Numpy array representation of the greyscale image
        :param threshold: Maximum value which to be mapped to 0, all above will be mapped to 1
        :return: Numpy array of the binary image
        '''

        bw_image = image.copy()
        numpy.subtract(bw_image, threshold)
        numpy.clip(bw_image, 0, 1)
        return bw_image

    def pil_to_numpyarray(self, image):
        return numpy.array(image)

    def numpyarray_to_pil(self, image):
        return Image.fromarray(numpy.uint8(image * 255))
