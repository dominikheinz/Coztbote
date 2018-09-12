import numpy
from Settings.CozmoSettings import Settings


class ImagePreprocessor:

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
