import numpy
from Engines.LaneTracking.GridField import GridField


class LaneAnalyzer:
    last_correction = 0

    def __init__(self):
        pass

    def calculate_lane_correction(self, image_grid):

        # Calculate black pixel ration for the bottom segments
        left_ratio = self.calc_black_pixel_ratio(image_grid.get_field(GridField.bottom_left))
        middle_ratio = self.calc_black_pixel_ratio(image_grid.get_field(GridField.bottom_middle))
        right_ratio = self.calc_black_pixel_ratio(image_grid.get_field(GridField.bottom_right))

        # Correction is 0 by default
        lane_correction = 0

        # Set correction if black pixel ration changes
        if left_ratio > middle_ratio * 0.8:
            lane_correction -= 1
        if right_ratio > middle_ratio * 0.8:
            lane_correction += 1

        # Return none if correction didnt change
        ret = None

        # Repeat last correct on lane depature
        if left_ratio + middle_ratio + right_ratio > 0.1 and self.last_correction != lane_correction:
            ret = lane_correction

            # Overwrite old correction with new one
            self.last_correction = lane_correction

        return ret

    @staticmethod
    def calc_black_pixel_ratio(img):
        return ((img.shape[0] * img.shape[1]) - numpy.sum(img)) / (img.shape[0] * img.shape[1])
