from Settings.CozmoSettings import Settings
from cozmo.util import degrees
from Utils.InstanceManager import InstanceManager
from Engines.RobotController.RobotStatusController import RobotStatusController
from Utils import TimingUtils


class SignHandler:
    RobotStatusController = None
    robot = None
    drive_controller = None

    def __init__(self):
        """
        Creating an instance of robot and getting the cooldown_time_ms from Settings.py
        """
        self.robot = InstanceManager.get_instance("Robot")
        self.lane_analyzer = InstanceManager.get_instance("CorrectionCalculator")
        self.drive_controller = InstanceManager.get_instance("DriveController")

    @staticmethod
    def finish_reaction_to_sign():
        RobotStatusController.disable_autonomous_behavior = False

    @staticmethod
    def trigger_sign_detection_cooldown():
        RobotStatusController.enable_sign_recognition = False

        def restart_detection():
            RobotStatusController.enable_sign_recognition = True

        TimingUtils.run_function_after(Settings.sign_detection_cooldown_time, restart_detection)

    def react_to_signs(self, sign_count):
        """
        Tells Cozmo what to do for every sign(amount of signs)
        :param sign_count: amount of spotted signs
        """
        if (sign_count % 2) == 1:
            # Handling for wrong identified signs, cause there als only even amount of signs
            print("ungerade")

        elif sign_count == 2:
            # Handling for two spotted signs
            SignHandler.trigger_sign_detection_cooldown()
            self.drive_controller.stop_autonomous_behaviour()
            TimingUtils.run_function_after(Settings.wait_time_sign1, SignHandler.finish_reaction_to_sign)

        elif sign_count == 4:
            # Handling for four spotted signs
            SignHandler.trigger_sign_detection_cooldown()
            self.drive_controller.stop_autonomous_behaviour()
            self.robot.turn_in_place(degrees(180), degrees(180))
            TimingUtils.run_function_after(1000 + 100, SignHandler.finish_reaction_to_sign)
