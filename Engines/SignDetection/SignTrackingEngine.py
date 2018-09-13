import datetime
from Utils.DebugUtils import DebugUtils
from Settings.CozmoSettings import Settings
from Engines.LaneTracking.ImagePreprocessor import ImagePreprocessor
from Utils.InstanceManager import InstanceManager


class SignTrackingEngine:
    robot = None
    drive_controller = None
    preview_utils = None
    sign_analyzer = None
    processor = None

    last_timestamp = None
    current_cam_frame = None

    def __init__(self):
        self.robot = InstanceManager.get_instance("Robot")
        self.drive_controller = InstanceManager.get_instance("DriveController")
        self.preview_utils = InstanceManager.get_instance("PreviewUtils")
        self.sign_analyzer = InstanceManager.get_instance("SignAnalyzer")

        self.last_timestamp = datetime.datetime.now()
        self.processor = ImagePreprocessor()

    def get_current_frame(self):
        return self.current_cam_frame

    def process_still_image(self, e, image):    # second parameter is always the event, saving it in 'e'
        # "Cool Down" for image processing, computing power cant keep up with the rate images arrive
        if self.last_timestamp < datetime.datetime.now() - datetime.timedelta(
                milliseconds=Settings.cozmo_framerate_limit):
            # tmr = DebugUtils.start_timer()
            # Convert image to black white
            img_bw = self.processor.rgb_to_bw(image.raw_image)  # already in binary form

            # Calculate lane correction based on image data
            lane_correction = self.lane_analyzer.calculate_lane_correction(img_bw)

            # If correction is required let cozmo correct
            if lane_correction is not None:
                self.drive_controller.correct(lane_correction)

            # Update current frame
            #self.current_cam_frame = img_bw * 255
            self.current_cam_frame = img_bw * 255

            # Show cam live preview if enabled
            if Settings.cozmo_show_cam_live_feed:
                self.preview_utils.show_cam_frame(img_bw)

            # Update timestamp
            self.last_timestamp = datetime.datetime.now()

            # tmr.stop_timer("process_still_image")
