import datetime
from Utils.DebugUtils import DebugUtils
from Settings.CozmoSettings import Settings
from Engines.LaneTracking.ImagePreprocessor import ImagePreprocessor
from Utils.InstanceManager import InstanceManager


class LaneTrackingEngine:
    robot = None
    drive_controller = None
    preview_utils = None
    lane_analyzer = None
    processor = None

    last_timestamp = None
    current_cam_frame = None

    def __init__(self):
        self.robot = InstanceManager.get_instance("Robot")
        self.drive_controller = InstanceManager.get_instance("DriveController")
        self.preview_utils = InstanceManager.get_instance("PreviewUtils")
        self.lane_analyzer = InstanceManager.get_instance("LaneAnalyzer")

        self.last_timestamp = datetime.datetime.now()
        self.processor = ImagePreprocessor()

    def get_current_frame(self):
        return self.current_cam_frame

    def process_still_image(self, e, image):
        if self.last_timestamp < datetime.datetime.now() - datetime.timedelta(
                milliseconds=Settings.cozmo_framerate_limit):
            # tmr = DebugUtils.start_timer()
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
                self.preview_utils.show_cam_frame(img_bw)

            # Update timestamp
            self.last_timestamp = datetime.datetime.now()

            # tmr.stop_timer("process_still_image")
