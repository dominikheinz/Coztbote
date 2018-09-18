import numpy
import math


class LaneAnalyzer:
    last_correction = 0
    last_points = None
    sign_count = 0
    sign_recognition_cooldown = False

    def __init__(self):
        pass

    def calculate_lane_correction(self, image):
        """
        Calculates a correction value between [-1..1], negative values meaning correct to the left,
        positive values to the right. The closer the value is to 0, the slighter the correction needs to be.
        :param image:
        :return:
        """

        x_row_1, x_row_2, x_row_3 = self.calculate_lane_correction_points(image)

        # Calculate center of image
        x_center = int(image.shape[1] / 2)

        # Set lane correction based on available points
        if x_row_1 is not None:
            lane_correction = -((x_center - x_row_1) / x_center)
        elif x_row_2 is not None:
            lane_correction = (-((x_center - x_row_2) / x_center)) * 1.4
        elif x_row_3 is not None:
            lane_correction = (-((x_center - x_row_3) / x_center)) * 1.8
        else:
            lane_correction = 1 if self.last_correction > 0 else -1

        self.last_correction = lane_correction

        return lane_correction

    def calculate_lane_correction_points(self, image):
        """
        Calculates three points which are on the lane
        :param image: Frame from Cozmos feed as numpy array
        :return: Three points on the lane
        :rtype: int, int, int
        """

        # Ensure unsigned values and make black nonzero and white zero
        image = numpy.array(image, dtype=numpy.uint8) - 1

        # Slices lower third of image into three evenly sized rows
        start_row_1 = int(image.shape[0] / 3)
        row_height = int((image.shape[0] - start_row_1) / 3)
        end_row_1 = start_row_1 + row_height
        end_row_2 = end_row_1 + row_height
        end_row_3 = image.shape[0]

        # Calculate center of all black pixels for each stripe
        x_row_1 = numpy.mean(numpy.nonzero(image[start_row_1:end_row_1])[1])
        x_row_2 = numpy.mean(numpy.nonzero(image[end_row_1:end_row_2])[1])
        x_row_3 = numpy.mean(numpy.nonzero(image[end_row_2:end_row_3])[1])

        # Invalidate when no black pixels were found
        x_row_1 = int(x_row_1) if not math.isnan(x_row_1) else None
        x_row_2 = int(x_row_2) if not math.isnan(x_row_2) else None
        x_row_3 = int(x_row_3) if not math.isnan(x_row_3) else None

        # Calculate coordinates of point on image
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

        # Update navigation point coordinates
        self.last_points = (row_1_point, row_2_point, row_3_point)

        return x_row_1, x_row_2, x_row_3
