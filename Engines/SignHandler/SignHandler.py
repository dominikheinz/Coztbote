import datetime
import time
from Settings.CozmoSettings import Settings
from cozmo.util import degrees
from Utils.InstanceManager import InstanceManager
from Engines.RobotController.RobotStatusController import RobotStatusController
from Engines.RobotController.DriveController import DriveController


class SignHandler:
    RobotStatusController = None
    robot = None

    def __init__(self):
        self.robot = InstanceManager.get_instance("Robot")
        self.cooldown_time = Settings.cooldown_time_ms

    def check_for_cooldown(self, time_sign_seen, disable_cooldown):
        """
        Checks last timestamp if time delta is exceeded, to block or 
        unblock sign_recognition_cooldown boolean
        :param time_sign_seen: time when sign is seen
        """

        if not disable_cooldown:
            if time_sign_seen < datetime.datetime.now() - datetime.timedelta(
                    milliseconds=self.cooldown_time) and RobotStatusController.sign_recognition_cooldown:
                RobotStatusController.sign_recognition_cooldown = False
                print("unblock")

            if RobotStatusController.sign_count != 0 and RobotStatusController.sign_recognition_cooldown==False:
                RobotStatusController.sign_recognition_cooldown = True
                #self.robot.turn_in_place(degrees(180))
                RobotStatusController.sign_count = 0
                print("should be blocked")

    def react_to_signs(self, sign_count):
        if (sign_count % 2) is 1:
            print("ungerade")

        elif sign_count is 2:
            print("2")
            DriveController.allow_driving = False
            RobotStatusController.action_start = datetime.datetime.now()
            RobotStatusController.action_cooldown_ms = Settings.wait_time_sign1

        elif sign_count is 4:
            print("4")
            DriveController.allow_driving = False
            self.robot.turn_in_place(degrees(180)).wait_for_completed()
            RobotStatusController.action_start = datetime.datetime.now()
            RobotStatusController.action_cooldown_ms = Settings.wait_time_sign2

        # self.check_driving_cooldown(RobotStatusController.action_start, RobotStatusController.action_cooldown_ms)

    def check_driving_cooldown(self):
        if RobotStatusController.action_start < datetime.datetime.now() - datetime.timedelta(
                milliseconds=RobotStatusController.action_cooldown_ms):
            DriveController.allow_driving = True
