import cv2
import numpy
from Engines.LaneTracking.CorrectionCalculator import LaneAnalyzer
from unittest import TestCase


class TestLaneAnalyzer(TestCase):

    def test_calculate_lane_correction_right(self):
        img = numpy.clip(cv2.imread("Resources/CalculateLaneCorrectionRight.png", cv2.IMREAD_GRAYSCALE), 0, 1)
        instance = LaneAnalyzer()
        data_out = instance.calculate_lane_correction(img)
        expected = 0.5
        self.assertGreater(data_out, expected)

    def test_calculate_lane_correction_left(self):
        img = numpy.clip(cv2.imread("Resources/CalculateLaneCorrectionLeft.png", cv2.IMREAD_GRAYSCALE), 0, 1)
        instance = LaneAnalyzer()
        data_out = instance.calculate_lane_correction(img)
        expected = -0.5
        self.assertLess(data_out, expected)

    def test_calculate_lane_correction_none(self):
        img = numpy.clip(cv2.imread("Resources/StraightLaneShape.png", cv2.IMREAD_GRAYSCALE), 0, 1)
        instance = LaneAnalyzer()
        data_out = instance.calculate_lane_correction(img)
        self.assertAlmostEqual(data_out, 0, places=2)
