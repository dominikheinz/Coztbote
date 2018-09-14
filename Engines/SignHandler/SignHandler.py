import datetime
from Settings.CozmoSettings import Settings
from cozmo.util import degrees
from Utils.InstanceManager import InstanceManager


class SignHandler:
    lane_analyzer = None
    robot = None
    last_timestamp = datetime.datetime.now()

    def __init__(self):
        self.lane_analyzer = InstanceManager.get_instance("LaneAnalyzer")
        self.robot = InstanceManager.get_instance("Robot")

    def do_something(self, last_timestamp):
        if last_timestamp < datetime.datetime.now() - datetime.timedelta(
                milliseconds=10000) and self.lane_analyzer.sign_recognition_cooldown:
            self.lane_analyzer.sign_recognition_cooldown = False
            print("unblock")

        if self.lane_analyzer.sign_count != 0 and self.lane_analyzer.sign_recognition_cooldown==False:
            self.lane_analyzer.sign_recognition_cooldown = True
            self.robot.turn_in_place(degrees(180))
            self.lane_analyzer.sign_count = 0
            print("should be blocked")

