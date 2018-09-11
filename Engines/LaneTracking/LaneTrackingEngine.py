from cv2 import *
import numpy
import datetime
from Engines.LaneTracking.PixelRow import PixelRow
from Engines.LaneTracking.ImagePreprocessor import ImagePreprocessor
from Engines.LaneTracking.LaneAnalyzer import LaneAnalyzer
from Settings.DebugUtils import DebugUtils
from Settings.CozmoSettings import Settings


class LaneTrackingEngine:
    robot = None
    drive_controller = None
    last_timestamp = None
    current_cam_frame = None

    processor = None
    lane_analyzer = None

    def __init__(self, robot, drive_controller):
        self.robot = robot
        self.drive_controller = drive_controller
        self.last_timestamp = datetime.datetime.now()

        self.processor = ImagePreprocessor()
        self.lane_analyzer = LaneAnalyzer()
        pass

    def get_current_frame(self):
        return self.current_cam_frame

    def process_still_image(self, e, image):
        if self.last_timestamp < datetime.datetime.now() - datetime.timedelta(milliseconds=200):

            # Convert image to black white
            img_bw = self.processor.rgb_to_bw(image.raw_image)

            # Update current frame
            self.current_cam_frame = img_bw * 255

            canny = cv2.Canny(img_bw, 100, 200)

            # Image segmentation
            rows_to_test = PixelRow.get_pixel_rows(canny)

            # Show cam live preview if enabled
            if Settings.cozmo_show_cam_live_feed:
                self.show_cam_frame(img_bw)

            # Calculate lane correction based on image data
            lane_correction = self.lane_analyzer.calculate_lane_correction(rows_to_test)

            # If correction is required let cozmo correct
            if lane_correction is not None:
                self.drive_controller.correct(lane_correction)

            # Update timestamp
            self.last_timestamp = datetime.datetime.now()

    def show_cam_frame(self, img_bw):
        tmr = DebugUtils.start_timer()
        cv2.imshow("Cam", numpy.multiply(img_bw, 65025))
        tmr.stop_timer("show_frame")
        cv2.waitKey(1)
