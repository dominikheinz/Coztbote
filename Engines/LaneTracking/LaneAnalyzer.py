import numpy
from Engines.LaneTracking.GridField import GridField


class LaneAnalyzer:
    last_correction = 0

    def __init__(self):
        pass

    def calculate_lane_correction(self, pixel_rows):

        # currently work only with one row
        row = pixel_rows[0]

        wanted_offset = row.wanted_offset

        lane_correction = wanted_offset - row.right_edge_offset
        lane_correction /= 320

        print("wanted offset: ", wanted_offset)
        print("left pos: ", row.left_edge_pos, '\t', "right pos: ", row.right_edge_pos)
        print("left offset: ", row.left_edge_offset, '\t', "right offset: ", row.right_edge_offset)

        return lane_correction

    @staticmethod
    def calc_black_pixel_ratio(img):
        return ((img.shape[0] * img.shape[1]) - numpy.sum(img)) / (img.shape[0] * img.shape[1])
