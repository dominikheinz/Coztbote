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
        img_bw = self.img_to_bw(img_gray)

        # Convert array to image
        return self.numpyarray_to_pil(img_bw)

    def img_to_bw(self, image):
        width, height = image.shape

        for w in range(0, width):
            for h in range(0, height):
                if image[w, h] > 60:
                    image[w, h] = 1
                else:
                    image[w, h] = 0
        return image

    def pil_to_numpyarray(self, image):
        return numpy.array(image)

    def numpyarray_to_pil(self, image):
        return Image.fromarray(numpy.uint8(image * 255))
