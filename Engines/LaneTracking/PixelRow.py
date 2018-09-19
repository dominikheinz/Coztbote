import numpy
from Utils.ImagePreprocessor import ImagePreprocessor

class PixelRow:

    pattern = numpy.array(0)  # e.g. [1, 0, 1]
    detailed_pattern = numpy.array(0)  # e.g. [[26, 1],[107, 0],[187, 1]]

    def __init__(self, raw_row):
        rle_data = ImagePreprocessor.run_length_encoding(raw_row)
        self.detailed_pattern = ImagePreprocessor.cleanup_row_noise(rle_data)
        self.pattern = self.detailed_pattern[:, 1]
