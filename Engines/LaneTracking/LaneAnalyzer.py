import numpy
import math
from Settings.DebugUtils import DebugUtils


class LaneAnalyzer:
    last_correction = 0
    last_points = None
    last_stripe_sums = None

    def __init__(self):
        pass

    def calculate_lane_correction(self, image):
        x_row_1, x_row_2, x_row_3 = self.calculate_lane_points(image)
        x_center = int(image.shape[1] / 2)
        if x_row_1 is not None:
            lane_correction = -((x_center - x_row_1) / x_center)
        elif x_row_2 is not None:
            lane_correction = (-((x_center - x_row_2) / x_center)) * 1.2
        elif x_row_3 is not None:
            lane_correction = (-((x_center - x_row_3) / x_center)) * 1.5
        else:
            lane_correction = 1 if self.last_correction > 0 else -1

        self.last_correction = lane_correction

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

        x_row_1 = numpy.mean(numpy.nonzero(image[start_row_1:end_row_1])[1])
        x_row_2 = numpy.mean(numpy.nonzero(image[end_row_1:end_row_2])[1])
        x_row_3 = numpy.mean(numpy.nonzero(image[end_row_2:end_row_3])[1])

        x_row_1 = int(x_row_1) if not math.isnan(x_row_1) else None
        x_row_2 = int(x_row_2) if not math.isnan(x_row_2) else None
        x_row_3 = int(x_row_3) if not math.isnan(x_row_3) else None

        row_1_point = (x_row_1, int((start_row_1 + end_row_1) / 2))
        row_2_point = (x_row_2, int((end_row_1 + end_row_2) / 2))
        row_3_point = (x_row_3, int((end_row_2 + end_row_3) / 2))

        # Presumably no lane visible
        if x_row_1 is None or numpy.count_nonzero(image[start_row_1:end_row_1]) < 1000:
            row_1_point = None
        if x_row_2 is None or numpy.count_nonzero(image[end_row_1:end_row_2]) < 1000:
            row_2_point = None
        if x_row_3 is None or numpy.count_nonzero(image[end_row_2:end_row_3]) < 1000:
            row_3_point = None

        self.last_points = (row_1_point, row_2_point, row_3_point)

        print(self.last_points)

        return x_row_1, x_row_2, x_row_3
