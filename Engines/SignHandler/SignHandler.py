import datetime
from Settings.CozmoSettings import Settings
from cozmo.util import degrees
from Utils.InstanceManager import InstanceManager


class SignHandler:
    lane_analyzer = None
    robot = None
    cooldown_time = None
    last_timestamp = datetime.datetime.now()

    def __init__(self):
        self.lane_analyzer = InstanceManager.get_instance("LaneAnalyzer")
        self.robot = InstanceManager.get_instance("Robot")
        self.cooldown_time = Settings.cooldown_time_ms

    def check_for_cooldown(self, time_sign_seen):
        """
        Checks last timestamp if time delta is exceeded, to block or 
        unblock sign_recognition_cooldown boolean
        :param time_sign_seen: time when sign is seen
        """
        if time_sign_seen < datetime.datetime.now() - datetime.timedelta(
                milliseconds=self.cooldown_time) and self.lane_analyzer.sign_recognition_cooldown:
            self.lane_analyzer.sign_recognition_cooldown = False
            print("unblock")

        if self.lane_analyzer.sign_count != 0 and self.lane_analyzer.sign_recognition_cooldown==False:
            self.lane_analyzer.sign_recognition_cooldown = True
            self.robot.turn_in_place(degrees(180))
            self.lane_analyzer.sign_count = 0
            print("should be blocked")

