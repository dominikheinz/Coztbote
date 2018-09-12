import cv2
import datetime
import os
from Settings.CozmoSettings import Settings
from Utils.Singleton import Singleton
from Utils.InstanceManager import InstanceManager


class PreviewUtils(metaclass=Singleton):
    laneanalyzer_obj = None
    robot_obj = None
    last_frame = None

    def __init__(self):
        self.lane_analyzer = InstanceManager.get_instance("LaneAnalyzer")
        self.robot_obj = InstanceManager.get_instance("Robot")

    def show_cam_frame(self, image):
        # Convert image from 0..1 to 0..255 and tri-channel
        image = cv2.cvtColor(image * 255, cv2.COLOR_GRAY2BGR)

        # Update last frame without points
        if not Settings.cozmo_preview_screenshot_include_points:
            self.last_frame = image

        # Draw navigation points
        if self.lane_analyzer.last_points[0] is not None:
            cv2.circle(image, self.lane_analyzer.last_points[0], radius=3, color=(255, 0, 0), thickness=5)
        if self.lane_analyzer.last_points[1] is not None:
            cv2.circle(image, self.lane_analyzer.last_points[1], radius=3, color=(0, 255, 0), thickness=5)
        if self.lane_analyzer.last_points[2] is not None:
            cv2.circle(image, self.lane_analyzer.last_points[2], radius=3, color=(0, 0, 255), thickness=5)

        # Resize preview window
        image = cv2.resize(image, Settings.cozmo_preview_resolution)

        # Update last frame with points
        if Settings.cozmo_preview_screenshot_include_points:
            self.last_frame = image

        # Display overlay text in preview window
        self.show_cam_overlay(image)

        # Show preview window
        cv2.imshow("Live Cam", image)
        cv2.waitKey(1)

    def save_cam_screenshot(self):
        desktop_path = os.path.expanduser("~/Desktop/")
        date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        cv2.imwrite(desktop_path + "Cozmo_" + date_string + ".png", self.last_frame)
        print("Screenshot", date_string, "saved")

    def show_cam_overlay(self, image):
        correction_text = ("Left" if self.lane_analyzer.last_correction < 0 else "Right")
        correction_text += " (" + str(self.lane_analyzer.last_correction) + ")"
        overlay_text_correction = "Correction: " + correction_text
        overlay_text_voltage = "Battery Voltage: " + str(round(self.robot_obj.battery_voltage, 1)) + "V"
        cv2.putText(image, overlay_text_correction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 128, 2)
        cv2.putText(image, overlay_text_voltage, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 128, 2)
