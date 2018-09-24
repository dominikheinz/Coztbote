import numpy
import cv2
from unittest import TestCase
from Engines.LaneAnalyzer.CrossingTypeIdentifier import CrossingTypeIdentifier
from Utils.ImagePreprocessor import ImagePreprocessor


class TestLaneSegmentIdentifier(TestCase):
    images = ["Resources/Lane_Curve_Left.png",
              "Resources/Lane_Curve_Right.png",
              "Resources/Lane_T_Crossing.png",
              "Resources/Lane_Crossing.png",
              "Resources/Lane_Right_T_Crossing.png",
              "Resources/Lane_Left_T_Crossing.png"]

    def test_filter_invalid_row_pattern(self):
        # Pattern of left t crossing with measurement error
        data_in = [[1, 0, 1], [1, 0, 1], [1, 0, 1], [0, 1], [0, 1], [0, 1], [1, 0, 1, 0, 1], [1, 0, 1], [1, 0, 1],
                   [1, 0, 1]]
        data_out = CrossingTypeIdentifier.filter_invalid_row_pattern(data_in)
        expected = [[1, 0, 1], [0, 1], [1, 0, 1]]
        numpy.testing.assert_array_equal(data_out, expected)

    def check_lane_types(self, function_ptr, correct_image_index):
        for i, img_path in enumerate(self.images):
            data_in = numpy.clip(cv2.imread(img_path, cv2.IMREAD_GRAYSCALE), 0, 1)
            pixel_rows = ImagePreprocessor.crop_image(data_in, top=90, right=10, bottom=30, left=10)
            pixel_rows = CrossingTypeIdentifier.create_row_patterns(pixel_rows)
            pixel_rows = CrossingTypeIdentifier.filter_invalid_row_pattern(pixel_rows)
            data_out = function_ptr(pixel_rows)

            if i == correct_image_index:
                self.assertTrue(data_out, function_ptr.__name__ + ": " + self.images[i])
            else:
                self.assertFalse(data_out, function_ptr.__name__ + ": " + self.images[i])

    def test_is_left_t_crossing(self):
        self.check_lane_types(CrossingTypeIdentifier.is_left_t_crossing, 5)

    def test_is_right_t_crossing(self):
        self.check_lane_types(CrossingTypeIdentifier.is_right_t_crossing, 4)

    def test_is_crossing(self):
        self.check_lane_types(CrossingTypeIdentifier.is_crossing, 3)
