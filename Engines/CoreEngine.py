import datetime
import cv2
from Settings.CozmoSettings import Settings
from Utils.InstanceManager import InstanceManager
from Utils.ImagePreprocessor import ImagePreprocessor
from Engines.RobotController.RobotStatusController import RobotStatusController
from Engines.LaneTracking.CrossingTypeIdentifier import CrossingTypeIdentifier


class CoreEngine:
    robot = None
    drive_controller = None
    preview_utils = None
    corr_calculator = None

    last_timestamp = None
    current_cam_frame = None
    cooldown_start = None

    def __init__(self):
        self.robot = InstanceManager.get_instance("Robot")
        self.drive_controller = InstanceManager.get_instance("DriveController")
        self.preview_utils = InstanceManager.get_instance("PreviewUtils")
        self.corr_calculator = InstanceManager.get_instance("CorrectionCalculator")
        self.sign_handler = InstanceManager.get_instance("SignHandler")
        self.navigator = InstanceManager.get_instance("Navigator")

        self.last_timestamp = datetime.datetime.now()

    def get_current_frame(self):
        """
        Gets the last processed frame
        :return: Processed image
        :rtype: Numpy array
        """
        return self.current_cam_frame

    def process_frame(self, image):
        """
        Processes the frame captured by Cozmos camera
        :param image: Current frame from Cozmos feed
        :type image: PIL image
        """
        # Convert image to binary
        bin_img = ImagePreprocessor.pil_rgb_to_numpy_binary(image)

        # Find contoures on image
        contours = ImagePreprocessor.find_contours(bin_img)

        # Extract lane shape and remove noise
        lane_img = ImagePreprocessor.extract_lane_shape(bin_img, contours)

        # Create image for later display
        display_img = cv2.cvtColor(lane_img * 255, cv2.COLOR_GRAY2BGR)

        # Counting signs and overwrite attribute in Lane Analyzer
        if RobotStatusController.enable_sign_recognition and \
                not Settings.disable_sign_detection and \
                not RobotStatusController.disable_autonomous_behavior:
            RobotStatusController.sign_count = ImagePreprocessor.calculate_number_of_signs(display_img, contours)
            self.sign_handler.react_to_signs(RobotStatusController.sign_count)

        if not RobotStatusController.disable_autonomous_behavior:
            crossing_type = CrossingTypeIdentifier.analyze_frame(lane_img)
            self.navigator.handle_crossing(crossing_type)

        if not RobotStatusController.disable_autonomous_behavior:
            # Calculate lane correction based on image data
            lane_correction = self.corr_calculator.calculate_lane_correction(lane_img)

            # If correction is required let Cozmo correct
            if lane_correction is not None:
                self.drive_controller.correct(lane_correction)

        # Update current frame
        self.current_cam_frame = display_img * 255

        # Show cam live preview if enabled
        if Settings.show_live_preview:
            self.preview_utils.show_cam_frame(display_img)
