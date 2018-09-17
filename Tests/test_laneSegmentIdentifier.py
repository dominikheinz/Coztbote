import numpy
import cv2
from unittest import TestCase
from Engines.LaneTracking.PixelRow import PixelRow
from Engines.LaneTracking.LaneSegmentIdentifier import LaneSegmentIdentifier


class TestLaneSegmentIdentifier(TestCase):
    images = ["Resources/Lane_Curve_Left.png",
              "Resources/Lane_Curve_Right.png",
              "Resources/Lane_T_Crossing.png",
              "Resources/Lane_Crossing.png",
              "Resources/Lane_Right_T_Crossing.png",
              "Resources/Lane_Left_T_Crossing.png"]

    # def test_create_pixel_rows(self):
    #     data_in = numpy.clip(cv2.imread("Resources/Lane_Fork_Clean.png", cv2.IMREAD_GRAYSCALE), 0, 1)
    #     data_out = LaneSegmentIdentifier.create_pixel_rows(data_in, 40)
    #     self.fail()

    def test_filter_invalid_row_pattern(self):
        # Pattern of left t crossing with measurement error
        data_in = [[1, 0, 1], [1, 0, 1], [1, 0, 1], [0, 1], [0, 1], [0, 1], [1, 0, 1, 0, 1], [1, 0, 1], [1, 0, 1],
                   [1, 0, 1]]
        data_out = LaneSegmentIdentifier.filter_invalid_row_pattern(data_in)
        expected = [[1, 0, 1], [0, 1], [1, 0, 1]]
        numpy.testing.assert_array_equal(data_out, expected)

    def test_is_left_t_crossing(self):
        correct_image_index = 5
        for i, img_path in enumerate(self.images):
            data_in = numpy.clip(cv2.imread(img_path, cv2.IMREAD_GRAYSCALE), 0, 1)
            pixel_rows = LaneSegmentIdentifier.crop_image(data_in)
            #cv2.imshow("Img", pixel_rows * 255)
            #cv2.waitKey(0)
            pixel_rows = LaneSegmentIdentifier.create_row_patterns(pixel_rows)
            pixel_rows = LaneSegmentIdentifier.filter_invalid_row_pattern(pixel_rows)
            data_out = LaneSegmentIdentifier.is_left_t_crossing(pixel_rows)
            if i == correct_image_index:
                self.assertTrue(data_out, self.images[i])
            else:
                self.assertFalse(data_out, self.images[i])


"""
    def test_is_right_t_crossing(self):
        correct_image_index = 4
        for i, img_path in enumerate(self.images):
            data_in = numpy.clip(cv2.imread(img_path, cv2.IMREAD_GRAYSCALE), 0, 1)
            pixel_rows = LaneSegmentIdentifier.create_row_patterns(data_in)
            data_out = LaneSegmentIdentifier.is_left_t_crossing(pixel_rows)
            if i == correct_image_index:
                self.assertTrue(data_out, self.images[i])
            else:
                self.assertFalse(data_out, self.images[i])

    def test_is_crossing(self):
        correct_image_index = 3
        for i, img_path in enumerate(self.images):
            data_in = numpy.clip(cv2.imread(img_path, cv2.IMREAD_GRAYSCALE), 0, 1)
            pixel_rows = LaneSegmentIdentifier.create_row_patterns(data_in)
            data_out = LaneSegmentIdentifier.is_left_t_crossing(pixel_rows)
            if i == correct_image_index:
                self.assertTrue(data_out, self.images[i])
            else:
                self.assertFalse(data_out, self.images[i])

    def test_is_t_crossing(self):
        correct_image_index = 2
        for i, img_path in enumerate(self.images):
            data_in = numpy.clip(cv2.imread(img_path, cv2.IMREAD_GRAYSCALE), 0, 1)
            pixel_rows = LaneSegmentIdentifier.create_row_patterns(data_in)
            data_out = LaneSegmentIdentifier.is_left_t_crossing(pixel_rows)
            if i == correct_image_index:
                self.assertTrue(data_out, self.images[i])
            else:
                self.assertFalse(data_out, self.images[i])
"""
