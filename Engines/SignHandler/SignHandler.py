from Settings.CozmoSettings import Settings
from Utils.InstanceManager import InstanceManager
from Controller.RobotStatusController import RobotStatusController
from Utils import TimingUtils


class SignHandler:
    RobotStatusController = None
    robot = None
    drive_controller = None
    behavior_controller = None

    def __init__(self):
        """
        Creating an instance of robot and getting the cooldown_time_ms from Settings.py
        """
        self.robot = InstanceManager.get_instance("Robot")
        self.correction_calculator = InstanceManager.get_instance("CorrectionCalculator")
        self.drive_controller = InstanceManager.get_instance("DriveController")
        self.behavior_controller = InstanceManager.get_instance("BehaviorController")

    @staticmethod
    def trigger_sign_detection_cooldown():
        RobotStatusController.enable_sign_recognition = False

        def restart_detection():
            RobotStatusController.enable_sign_recognition = True

        TimingUtils.run_function_after(Settings.sign_detection_cooldown_ms, restart_detection)

    def react_to_signs(self, sign_count):
        """
        Tells Cozmo what to do for every sign (amount of signs)
        :param sign_count: amount of spotted signs
        """
        if (sign_count % 2) == 1:
            # Handling for falsely identified signs, because only even amounts of signs are valid
            print("Odd_Sign_Count_Error")

        elif sign_count == 2:
            # Handling for two spotted signs
            if RobotStatusController.is_holding_cube:
                print("Noise detected")
            else:
                self.behavior_controller.run_packet_station_behaviour()

        elif sign_count == 4:
            # Handling for four spotted signs
            self.behavior_controller.run_face_matching_behavior()

        elif sign_count == 6:
            # Handling for six spotted signs
            SignHandler.trigger_sign_detection_cooldown()
            self.drive_controller.turn_around()
