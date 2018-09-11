from cv2 import *
import numpy
import datetime
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
        if self.last_timestamp < datetime.datetime.now() - datetime.timedelta(
                milliseconds=Settings.cozmo_framerate_limit):
            tmr = DebugUtils.start_timer()
            # Convert image to black white
            img_bw = self.processor.rgb_to_bw(image.raw_image)

            # Calculate lane correction based on image data
            lane_correction = self.lane_analyzer.calculate_lane_correction(img_bw)

            # If correction is required let cozmo correct
            if lane_correction is not None:
                self.drive_controller.correct(lane_correction)

            # Update current frame
            self.current_cam_frame = img_bw * 255

            # Show cam live preview if enabled
            if Settings.cozmo_show_cam_live_feed:
                self.show_cam_frame(img_bw, self.lane_analyzer.last_points)

            # Update timestamp
            self.last_timestamp = datetime.datetime.now()

            tmr.stop_timer()

    def show_cam_frame(self, image, lane_analyzer_dots):
        image = cv2.cvtColor(image * 255, cv2.COLOR_GRAY2BGR)
        # img_bw = self.print_dots(img_bw)
        if lane_analyzer_dots[0] is not None:
            cv2.circle(image, lane_analyzer_dots[0], radius=3, color=(255, 0, 0), thickness=5)
        if lane_analyzer_dots[1] is not None:
            cv2.circle(image, lane_analyzer_dots[1], radius=3, color=(0, 255, 0), thickness=5)
        if lane_analyzer_dots[2] is not None:
            cv2.circle(image, lane_analyzer_dots[2], radius=3, color=(0, 0, 255), thickness=5)

        image = cv2.resize(image, (1080, 720))
        cv2.imshow("Cam", image)
        cv2.waitKey(1)
