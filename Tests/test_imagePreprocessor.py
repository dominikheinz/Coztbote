import numpy
from unittest import TestCase
from Engines.LaneTracking.ImagePreprocessor import ImagePreprocessor


class TestImagePreprocessor(TestCase):

    def test_run_length_encoding_normal_array(self):
        data_in = numpy.array([1, 1, 3, 2, 3, 3, 3, 2, 2, 1, 4, 4])
        data_out = ImagePreprocessor.run_length_encoding(data_in)
        expected = numpy.array([[2, 1], [1, 3], [1, 2], [3, 3], [2, 2], [1, 1], [2, 4]])
        numpy.testing.assert_array_equal(data_out, expected)

    def test_run_length_encoding_empty(self):
        data_in = numpy.array([])
        data_out = ImagePreprocessor.run_length_encoding(data_in)
        expected = numpy.array([])
        numpy.testing.assert_array_equal(data_out, expected)

    def test_cleanup_row_noise_invalid_middle(self):
        data_in = numpy.array([[7,1],[2,0],[12,1],[9,0],[12,1]])
        data_out = ImagePreprocessor.cleanup_row_noise(data_in, 6)
        expected = numpy.array([[21,1],[9,0],[12,1]])
        numpy.testing.assert_array_equal(data_out, expected)

    def test_cleanup_row_noise_double_invalid_middle(self):
        data_in = numpy.array([[7,1],[2,0],[3,1],[9,0],[12,1]])
        data_out = ImagePreprocessor.cleanup_row_noise(data_in, 6)
        expected = numpy.array([[12,1],[9,0],[12,1]])
        numpy.testing.assert_array_equal(data_out, expected)

    def test_cleanup_row_noise_invalid_prefix(self):
        data_in = numpy.array([[3,1],[2,0],[12,1],[9,0],[12,1]])
        data_out = ImagePreprocessor.cleanup_row_noise(data_in, 6)
        expected = numpy.array([[17,1],[9,0],[12,1]])
        numpy.testing.assert_array_equal(data_out, expected)

    def test_cleanup_row_noise_invalid_suffix(self):
        data_in = numpy.array([[7,1],[8,0],[12,1],[9,0],[4,1]])
        data_out = ImagePreprocessor.cleanup_row_noise(data_in, 6)
        expected = numpy.array([[7,1],[8,0],[12,1],[13,0]])
        numpy.testing.assert_array_equal(data_out, expected)
