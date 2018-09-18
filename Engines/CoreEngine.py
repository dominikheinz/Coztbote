import datetime
from Settings.CozmoSettings import Settings
from Utils.InstanceManager import InstanceManager
from Utils.ImagePreprocessor import ImagePreprocessor
from Engines.RobotController.RobotStatusController import RobotStatusController
from Engines.LaneTracking.CrossingTypeIdentifier import CrossingTypeIdentifier


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
        self.drive_controller = InstanceManager.get_instance("DriveController")
        self.preview_utils = InstanceManager.get_instance("PreviewUtils")
        self.lane_analyzer = InstanceManager.get_instance("LaneAnalyzer")
        self.sign_handler = InstanceManager.get_instance("SignHandler")
        self.navigator_controller = InstanceManager.get_instance("NavigatorController")

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

            # Convert image to binary
            bin_img = ImagePreprocessor.pil_rgb_to_numpy_binary(image)

            # Counting signs and overwrite attribute in Lane Analyzer
            # if not RobotStatusController.is_at_crossing:
            #     if not self.lane_analyzer.sign_recognition_cooldown:
            #         self.lane_analyzer.sign_count = ImagePreprocessor.calculate_number_of_signs(bin_img)
            #         self.cooldown_start = datetime.datetime.now()

            # Extract lane shape and remove noise
            bin_img, bin_surroundings = ImagePreprocessor.extract_lane_shape(bin_img)

            if not RobotStatusController.is_at_crossing:

                crossing_type = CrossingTypeIdentifier.analyze_frame(bin_img)
                self.navigator_controller.handle_crossing(crossing_type)

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

            # Check if cooldown has expired
            # self.sign_handler.check_for_cooldown(self.cooldown_start)
