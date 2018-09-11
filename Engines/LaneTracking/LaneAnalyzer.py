import numpy
from Settings.DebugUtils import DebugUtils


class LaneAnalyzer:
    last_correction = 0
    last_points = None

    def __init__(self):
        pass

    def calculate_lane_correction(self, image):
        x_row_1, x_row_2, x_row_3 = self.calculate_lane_points(image)
        x_center = int(image.shape[1] / 2)
        immediate_lane_correction = (x_center - x_row_1) / x_center / 10
        future_lane_correction = (x_center - x_row_2) / x_center / 10

        lane_correction = (immediate_lane_correction * 2 + future_lane_correction) / 3

        return lane_correction

    def calculate_lane_points(self, image):
        """
        Calculates three points which are on the lane
        :param image: Frame from Cozmos feed
        :return: Three points on the lane
        """
        image = numpy.array(image, dtype=numpy.uint8) - 1

        start_row_1 = int(image.shape[0] / 3)
        row_height = int((image.shape[0] - start_row_1) / 3)
        end_row_1 = start_row_1 + row_height
        end_row_2 = end_row_1 + row_height
        end_row_3 = image.shape[0]

        x_row_1 = int(numpy.mean(numpy.nonzero(image[start_row_1:end_row_1])[1]))
        x_row_2 = int(numpy.mean(numpy.nonzero(image[end_row_1:end_row_2])[1]))
        x_row_3 = int(numpy.mean(numpy.nonzero(image[end_row_2:end_row_3])[1]))

        self.last_points = (
            (x_row_1, int((start_row_1 + end_row_1) / 2)),
            (x_row_2, int((end_row_1 + end_row_2) / 2)),
            (x_row_3, int((end_row_2 + end_row_3) / 2))
        )

        return x_row_1, x_row_2, x_row_3
