import numpy
from unittest import TestCase
from Engines.LaneTracking.ImagePreprocessor import ImagePreprocessor


class TestImagePreprocessor(TestCase):

    def test_run_length_encoding_normal_array(self):
        data_in = [1, 1, 3, 2, 3, 3, 3, 2, 2, 1, 4, 4]
        data_out = ImagePreprocessor.run_length_encoding(data_in)
        expected = numpy.array([[2, 1], [1, 3], [1, 2], [3, 3], [2, 2], [1, 1], [2, 4]])
        self.assertEqual(data_out.all(), expected.all())

    def test_run_length_encoding_empty(self):
        data_in = []
        data_out = ImagePreprocessor.run_length_encoding(data_in)
        expected = numpy.array([])
        self.assertEqual(data_out.all(), expected.all())

