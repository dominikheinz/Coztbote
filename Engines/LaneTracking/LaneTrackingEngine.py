import datetime
from Settings.CozmoSettings import Settings
from Utils.InstanceManager import InstanceManager
from Utils.DebugUtils import DebugUtils
from Engines.LaneTracking.ImagePreprocessor import ImagePreprocessor
from Engines.SignHandler import SignHandler

class LaneTrackingEngine:
    robot = None
    drive_controller = None
    preview_utils = None
    lane_analyzer = None

    last_timestamp = None
    current_cam_frame = None
    cooldown_start = None

    def __init__(self):
        self.robot = InstanceManager.get_instance("Robot")
        self.drive_controller = InstanceManager.get_instance("RobotController")
        self.preview_utils = InstanceManager.get_instance("PreviewUtils")
        self.lane_analyzer = InstanceManager.get_instance("LaneAnalyzer")

        self.last_timestamp = datetime.datetime.now()

    def get_current_frame(self):
        """
        Gets the last processed frame
        :return: Processed image
        :rtype: Numpy array
        """
        return self.current_cam_frame

    def process_frame(self, e, image):
        """
        Processes the frame captured by Cozmos camera
        :param e: Event object, which gets passed to this function by the event handler
        :param image: Current frame from Cozmos feed
        :type image: PIL image
        """
        # "Cooldown", so a frame can only be processed each x milliseconds, other frames are discarded
        if self.last_timestamp < datetime.datetime.now() - datetime.timedelta(
                milliseconds=Settings.cozmo_img_processing_ms_limit):
            tmr = DebugUtils.start_timer()
            # Convert image to binary
            bin_img = ImagePreprocessor.pil_rgb_to_numpy_binary(image.raw_image)

            # Extract lane shape and remove noise

            bin_img = ImagePreprocessor.extract_lane_shape(bin_img)

            # Calculate lane correction based on image data
            lane_correction = self.lane_analyzer.calculate_lane_correction(bin_img)

            # If correction is required let Cozmo correct
            if lane_correction is not None:
                self.drive_controller.correct(lane_correction)

            # Update current frame
            self.current_cam_frame = bin_img * 255

            # Show cam live preview if enabled
            if Settings.cozmo_show_cam_live_feed:
                self.preview_utils.show_cam_frame(bin_img)

            # Update timestamp
            self.last_timestamp = datetime.datetime.now()

            DebugUtils.stop_timer(tmr, "extract_lane_shape")
