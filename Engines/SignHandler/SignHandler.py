import datetime
from Settings.CozmoSettings import Settings
from cozmo.util import degrees
from Utils.InstanceManager import InstanceManager
from Engines.RobotController.RobotStatusController import RobotStatusController
from Engines.RobotController.DriveController import DriveController


class SignHandler:
    RobotStatusController = None
    robot = None

    def __init__(self):
        """
        Creating an instance of robot and getting the cooldown_time_ms from Settings.py
        """
        self.robot = InstanceManager.get_instance("Robot")
        self.cooldown_time = Settings.cooldown_time_ms

    def check_for_cooldown(self, time_sign_seen, disable_cooldown):
        """
        Checks last timestamp if time delta is exceeded, to block or 
        unblock sign_recognition_cooldown boolean
        :param time_sign_seen: time when sign is seen
        :param disable_cooldown: bool to disable cooldown functionality
        """

        if not disable_cooldown:
            # Checks if time interval is big enough to unlock the sign_recognition_cooldown
            if time_sign_seen < datetime.datetime.now() - datetime.timedelta(
                    milliseconds=self.cooldown_time) and RobotStatusController.sign_recognition_cooldown:
                RobotStatusController.sign_recognition_cooldown = False
                print("unblock")

            # Sets the cooldown for sign recognition if signs were seen, to prevent action looping
            if RobotStatusController.sign_count != 0 and RobotStatusController.sign_recognition_cooldown is not False:
                RobotStatusController.sign_recognition_cooldown = True
                RobotStatusController.sign_count = 0    # Setting sign count to zero to prevent action looping
                print("should be blocked")

    def react_to_signs(self, sign_count):
        """
        Tells Cozmo what to do for every sign(amount of signs)
        :param sign_count: amount of spotted signs
        """
        if (sign_count % 2) is 1:
            # Handling for wrong identified signs, cause there als only even amount of signs
            print("ungerade")

        elif sign_count is 2:
            # Handling for two spotted signs
            DriveController.allow_driving = False
            RobotStatusController.action_start = datetime.datetime.now()
            RobotStatusController.action_cooldown_ms = Settings.wait_time_sign1

        elif sign_count is 4:
            # Handling for four spotted signs
            DriveController.allow_driving = False
            self.robot.turn_in_place(degrees(180)).wait_for_completed()
            RobotStatusController.action_start = datetime.datetime.now()
            RobotStatusController.action_cooldown_ms = Settings.wait_time_sign2

        # self.check_driving_cooldown(RobotStatusController.action_start, RobotStatusController.action_cooldown_ms)

    def check_driving_cooldown(self):
        """
        Checks remaining cooldown time, to allow driving
        :return:
        """
        if RobotStatusController.action_start < datetime.datetime.now() - datetime.timedelta(
                milliseconds=RobotStatusController.action_cooldown_ms):
            DriveController.allow_driving = True
