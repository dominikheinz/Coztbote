import cv2
import numpy
from Engines.LaneTracking.CorrectionCalculator import CorrectionCalculator
from unittest import TestCase


class TestLaneAnalyzer(TestCase):

    def test_calculate_lane_correction_right(self):
        img = numpy.clip(cv2.imread("Resources/Lane_Curve_Right.png", cv2.IMREAD_GRAYSCALE), 0, 1)
        instance = CorrectionCalculator()
        data_out = instance.calculate_lane_correction(img)
        expected = 0.5
        self.assertGreater(data_out, expected)

    def test_calculate_lane_correction_left(self):
        img = numpy.clip(cv2.imread("Resources/Lane_Curve_Left.png", cv2.IMREAD_GRAYSCALE), 0, 1)
        instance = CorrectionCalculator()
        data_out = instance.calculate_lane_correction(img)
        expected = -0.5
        self.assertLess(data_out, expected)

    def test_calculate_lane_correction_none(self):
        img = numpy.clip(cv2.imread("Resources/Lane_Straight.png", cv2.IMREAD_GRAYSCALE), 0, 1)
        instance = CorrectionCalculator()
        data_out = instance.calculate_lane_correction(img)
        self.assertAlmostEqual(data_out, 0, places=2)
