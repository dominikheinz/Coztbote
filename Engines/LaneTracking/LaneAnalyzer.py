import numpy
from Engines.LaneTracking.GridField import GridField


class LaneAnalyzer:

    def __init__(self):
        pass

    def calculate_lane_correction(self, image_grid):
        left_ratio = self.calc_black_pixel_ratio(image_grid.get_field(GridField.bottom_left))
        middle_ratio = self.calc_black_pixel_ratio(image_grid.get_field(GridField.bottom_middle))
        right_ratio = self.calc_black_pixel_ratio(image_grid.get_field(GridField.bottom_right))

        lane_correction = 0

        if left_ratio > middle_ratio * 0.8:
            lane_correction -= 3
        if right_ratio > middle_ratio * 0.8:
            lane_correction += 3

        return lane_correction

    @staticmethod
    def calc_black_pixel_ratio(image):
        return ((image.shape[0] * image.shape[1]) - numpy.sum(image)) / (image.shape[0] * image.shape[1])
