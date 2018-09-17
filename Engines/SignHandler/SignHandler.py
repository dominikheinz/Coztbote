import datetime
from Settings.CozmoSettings import Settings
from cozmo.util import degrees
from Utils.InstanceManager import InstanceManager
from Engines.RobotController.RobotStatusController import RobotStatusController


class SignHandler:
    RobotStatusController = None
    robot = None
    cooldown_time = None
    last_timestamp = datetime.datetime.now()

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

