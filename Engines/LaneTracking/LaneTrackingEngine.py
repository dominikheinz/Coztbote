from cv2 import *
import numpy
import datetime
from Engines.LaneTracking.ImageGrid import ImageGrid
from Engines.LaneTracking.ImagePreprocessor import ImagePreprocessor
from Engines.LaneTracking.LaneAnalyzer import LaneAnalyzer
from Settings.DebugUtils import DebugUtils


class LaneTrackingEngine:
    robot = None
    drive_controller = None
    last_timestamp = None

    processor = None
    lane_analyzer = None

    def __init__(self, robot, drive_controller):
        self.robot = robot
        self.drive_controller = drive_controller
        self.last_timestamp = datetime.datetime.now()

        self.processor = ImagePreprocessor()
        self.lane_analyzer = LaneAnalyzer()
        pass

    def process_still_image(self, e, image):
        if self.last_timestamp < datetime.datetime.now() - datetime.timedelta(milliseconds=200):
            img_raw = image.raw_image
            img_bw = self.processor.rgb_to_bw(img_raw)

            image_grid = ImageGrid(img_bw)

            self.show_frame(img_bw)

            lane_correction = self.lane_analyzer.calculate_lane_correction(image_grid)
            print("Correction:", lane_correction)

            if lane_correction is not None:
                self.drive_controller.correct(lane_correction)

            self.last_timestamp = datetime.datetime.now()

    def show_frame(self, img_bw):
        cv2.imshow("Cam", numpy.multiply(img_bw, 255 * 255))
        cv2.waitKey(1)
