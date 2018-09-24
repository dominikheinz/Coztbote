import cv2
import datetime
import os
import numpy

from Engines.Navigation.Navigator import Navigator
from Settings.CozmoSettings import Settings
from Utils.Singleton import Singleton
from Utils.InstanceManager import InstanceManager
from Engines.LaneAnalyzer.CrossingType import CrossingType
from Engines.LaneAnalyzer.CrossingTypeIdentifier import CrossingTypeIdentifier
from Controller.RobotStatusController import RobotStatusController


class PreviewUtils(metaclass=Singleton):
    last_frame = None

    current_destination = 0
    current_cube_owner = None

    def __init__(self):
        self.correction_calculator_obj = InstanceManager.get_instance("CorrectionCalculator")
        self.robot_obj = InstanceManager.get_instance("Robot")

    def show_cam_frame(self, image):
        """
        Show the current frame in a window
        :param image: Image to show
        :type image: Numpy array
        """

        if Settings.live_preview_show_crossing_detection_region:
            cv2.rectangle(image, (Settings.crossing_left_crop, Settings.crossing_top_crop),
                          (image.shape[1] - Settings.crossing_right_crop,
                           image.shape[0] - Settings.crossing_bottom_crop),
                          color=(113, 204, 46), thickness=1)

        # Update last frame without points
        if not Settings.live_preview_screenshot_include_points:
            self.last_frame = image.copy()

        # Draw navigation points
        if self.correction_calculator_obj.last_points is not None and \
                not RobotStatusController.disable_autonomous_behavior:
            if self.correction_calculator_obj.last_points[0] is not None:
                cv2.circle(image, self.correction_calculator_obj.last_points[0],
                           radius=3, color=(255, 0, 0), thickness=5)
            if self.correction_calculator_obj.last_points[1] is not None:
                cv2.circle(image, self.correction_calculator_obj.last_points[1],
                           radius=3, color=(0, 255, 0), thickness=5)
            if self.correction_calculator_obj.last_points[2] is not None:
                cv2.circle(image, self.correction_calculator_obj.last_points[2],
                           radius=3, color=(0, 0, 255), thickness=5)

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

    @staticmethod
    def show_preview_text(text):
        img = numpy.zeros((240, 320), dtype=numpy.uint8)

        font = cv2.FONT_HERSHEY_SIMPLEX

        # get boundary of this text
        text_size = cv2.getTextSize(text, font, 1, 2)[0]

        # get coords based on boundary
        text_x = int((img.shape[1] - text_size[0]) / 2)
        text_y = int((img.shape[0] + text_size[1]) / 2)

        # add text centered on image
        cv2.putText(img, text, (text_x, text_y), font, 1, (255, 255, 255), 2)

        # Resize
        img = cv2.resize(img, Settings.live_preview_resolution, interpolation=cv2.INTER_NEAREST)

        cv2.imshow("Live Cam", img)
        cv2.waitKey(1)

    def apply_info_overlay(self, image):
        """
        Applies an overlay with debug info on an image
        :param image: The image to apply to
        :type image: Numpy array
        """
        correction_text = ("Left" if self.correction_calculator_obj.last_correction < 0 else "Right")
        correction_text += " (" + str(round(self.correction_calculator_obj.last_correction, 2)) + ")"
        overlay_text_correction = "Correction: " + correction_text
        overlay_text_voltage = "Battery Voltage: " + str(round(self.robot_obj.battery_voltage, 1)) + "V"
        overlay_lane_type = "Lane Type: " + str(
            CrossingType.get_crossing_as_string(CrossingTypeIdentifier.last_crossing_type))
        overlay_text_signs = "Amount of Signs: " + str(RobotStatusController.sign_count)
        overlay_color_signs = 128 if RobotStatusController.enable_sign_recognition else (220, 220, 220)
        overlay_text_destination = "Destination: " + ("Packetstation" if Navigator.current_end == 0
                                                      else "House " + str(Navigator.current_end))
        if not self.current_destination == Navigator.current_end:
            self.current_cube_owner = ""
            for owner_name in Settings.owner_dict:
                if Settings.owner_dict[owner_name] == RobotStatusController.holding_cube_id:
                    if not self.current_cube_owner == "":
                        self.current_cube_owner += ", "
                    self.current_cube_owner += "Herr " + owner_name
            self.current_destination = Navigator.current_end
        overlay_text_cube_owner = "Cube Owner: " + str(self.current_cube_owner)
        cv2.putText(image, overlay_text_correction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 128, 2)
        cv2.putText(image, overlay_text_voltage, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 128, 2)
        cv2.putText(image, overlay_text_signs, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, overlay_color_signs, 2)
        cv2.putText(image, overlay_lane_type, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 128, 2)
        cv2.putText(image, overlay_text_destination, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 128, 2)
        cv2.putText(image, overlay_text_cube_owner, (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 128, 2)
