import numpy
from Settings.CozmoSettings import Settings
from Engines.LaneTracking.ImagePreprocessor import ImagePreprocessor


class PixelRow:
    pattern = None

    def __init__(self, raw_row):
        rle_data = ImagePreprocessor.run_length_encoding(raw_row)
        rle_data = ImagePreprocessor.cleanup_row_noise(rle_data)

        
