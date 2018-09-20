import cv2
import datetime
import os
from Settings.CozmoSettings import Settings
from Utils.Singleton import Singleton
from Utils.InstanceManager import InstanceManager
from Engines.LaneTracking.CrossingType import CrossingType
from Engines.LaneTracking.CrossingTypeIdentifier import CrossingTypeIdentifier
from Engines.RobotController.RobotStatusController import RobotStatusController


class PreviewUtils(metaclass=Singleton):
    last_frame = None

    def __init__(self):
        self.lane_analyzer_obj = InstanceManager.get_instance("CorrectionCalculator")
        self.robot_obj = InstanceManager.get_instance("Robot")

    def show_cam_frame(self, image):
        """
        Show the current frame in a window
        :param image: Image to show
        :type image: Numpy array
        """
        # Update last frame without points
        if not Settings.live_preview_screenshot_include_points:
            self.last_frame = image.copy()

        # Draw navigation points
        if self.lane_analyzer_obj.last_points is not None and \
                not RobotStatusController.disable_autonomous_behavior:
            if self.lane_analyzer_obj.last_points[0] is not None:
                cv2.circle(image, self.lane_analyzer_obj.last_points[0], radius=3, color=(255, 0, 0), thickness=5)
            if self.lane_analyzer_obj.last_points[1] is not None:
                cv2.circle(image, self.lane_analyzer_obj.last_points[1], radius=3, color=(0, 255, 0), thickness=5)
            if self.lane_analyzer_obj.last_points[2] is not None:
                cv2.circle(image, self.lane_analyzer_obj.last_points[2], radius=3, color=(0, 0, 255), thickness=5)

        # Update last frame with points
        if Settings.live_preview_screenshot_include_points:
            self.last_frame = image.copy()

        # Resize preview window
        image = cv2.resize(image, Settings.live_preview_resolution, interpolation=cv2.INTER_NEAREST)

        # Display overlay text in preview window
        self.apply_info_overlay(image)

        # Show preview window
        cv2.imshow("Live Cam", image)
        cv2.waitKey(1)

    def save_cam_screenshot(self):
        """
        Save current frame as PNG to desktop
        """
        desktop_path = os.path.expanduser("~/Desktop/")
        date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        cv2.imwrite(desktop_path + "Cozmo_" + date_string + ".png", self.last_frame)
        print("Screenshot", date_string, "saved")

    def apply_info_overlay(self, image):
        """
        Applies an overlay with debug info on an image
        :param image: The image to apply to
        :type image: Numpy array
        """
        correction_text = ("Left" if self.lane_analyzer_obj.last_correction < 0 else "Right")
        correction_text += " (" + str(round(self.lane_analyzer_obj.last_correction, 2)) + ")"
        overlay_text_correction = "Correction: " + correction_text
        overlay_text_voltage = "Battery Voltage: " + str(round(self.robot_obj.battery_voltage, 1)) + "V"
        overlay_lane_type = "Lane Type: " + str(
            CrossingType.get_crossing_as_string(CrossingTypeIdentifier.last_crossing_type))
        overlay_text_signs = "Amount of Signs: " + str(RobotStatusController.sign_count)
        overlay_color_signs = 128 if RobotStatusController.enable_sign_recognition else (220, 220, 220)
        cv2.putText(image, overlay_text_correction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 128, 2)
        cv2.putText(image, overlay_text_voltage, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 128, 2)
        cv2.putText(image, overlay_text_signs, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, overlay_color_signs, 2)
        cv2.putText(image, overlay_lane_type, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 128, 2)
