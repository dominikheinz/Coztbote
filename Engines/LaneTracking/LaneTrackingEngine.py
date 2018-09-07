from cv2 import *
import numpy
import datetime
from Engines.LaneTracking.ImageGrid import ImageGrid
from Engines.LaneTracking.ImagePreprocessor import ImagePreprocessor
from Engines.LaneTracking.LaneAnalyzer import LaneAnalyzer


class LaneTrackingEngine:
    robot = None
    drive_controller = None
    last_timestamp = None
    last_correction = 0

    def __init__(self, robot, drive_controller):
        self.robot = robot
        self.drive_controller = drive_controller
        self.last_timestamp = datetime.datetime.now()
        pass

    def process_still_image(self, e, image):
        if self.last_timestamp < datetime.datetime.now() - datetime.timedelta(milliseconds=200) \
                or self.drive_controller.is_turning:
            processor = ImagePreprocessor()
            img_raw = image.raw_image
            img_bw = processor.rgb_to_bw(img_raw)

            image_grid = ImageGrid(img_bw)
            lane_analyzer = LaneAnalyzer()

            cv2.imshow("Cam", numpy.multiply(img_bw, 255 * 255))
            cv2.waitKey(1)

            lane_correction = lane_analyzer.calculate_lane_correction(image_grid)
            print("Correction:", lane_correction)

            if lane_correction != self.last_correction:
                self.drive_controller.correct(lane_correction)
                self.last_correction = lane_correction

            self.last_timestamp = datetime.datetime.now()
