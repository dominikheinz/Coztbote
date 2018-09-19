import unittest
import cv2, numpy
from unittest import TestCase
from Utils.ImagePreprocessor import ImagePreprocessor


class TestSignRecognition(TestCase):

    def test_for_four(self):
        four_allowed = 1-numpy.clip(cv2.imread("Resources/four_allowed.png", cv2.IMREAD_GRAYSCALE), 0, 1)

        number_of_recognized_signs1 = ImagePreprocessor.calculate_number_of_signs(four_allowed)

        self.assertEqual(4, number_of_recognized_signs1)

    def test_for_2(self):
        four_not_allowed = 1 - numpy.clip(cv2.imread("Resources/two_allowed.png", cv2.IMREAD_GRAYSCALE), 0, 1)

        number_of_recognized_signs2 = ImagePreprocessor.calculate_number_of_signs(four_not_allowed)

        self.assertEqual(2, number_of_recognized_signs2)

    def test_if_odd(self):
        two_allowed = 1 - numpy.clip(cv2.imread("Resources/odd.png", cv2.IMREAD_GRAYSCALE), 0, 1)

        number_of_recognized_signs = ImagePreprocessor.calculate_number_of_signs(two_allowed)
        number_of_recognized_signs = number_of_recognized_signs % 2

        self.assertEqual(1, number_of_recognized_signs)


if __name__ == '__main__':
    unittest.main()
