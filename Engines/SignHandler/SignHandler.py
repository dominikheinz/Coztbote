from cozmo.util import degrees
from Utils.InstanceManager import InstanceManager


class SignHandler:
    lane_analyzer = None
    robot = None

    def __init__(self):
        self.lane_analyzer = InstanceManager.get_instance("LaneAnalyzer")
        self.robot = InstanceManager.get_instance("Robot")

    def do_something(self):
        if self.lane_analyzer.sign_count != 0:
            self.lane_analyzer.sign_recognition_cooldown = True
            self.robot.turn_in_place(degrees(180)).wait_for_complete()
            self.lane_analyzer.sign_recognition_cooldown = False
