from Engines.LaneTracking.CrossingType import CrossingType
from Utils.InstanceManager import InstanceManager
from Engines.RobotController import RobotStatusController


class NavigatorController:

    def __init__(self):
        self.drive_controller = InstanceManager.get_instance("DriveController")

    def handle_crossing(self, crossing_type):
        if crossing_type == CrossingType.Crossing:
            self.drive_controller.crossing_go_straight() # ToDo Change Direction
        elif crossing_type == CrossingType.T_Crossing:
            self.drive_controller.crossing_turn_left() # ToDo Change Direction
        elif crossing_type == CrossingType.Right_T_Crossing:
            self.drive_controller.crossing_turn_right() # ToDo Change Direction
        elif crossing_type == CrossingType.Left_T_Crossing:
            self.drive_controller.crossing_turn_left() # ToDo Change Direction
        else:
            RobotStatusController.is_at_crossing = False
            self.drive_controller.start()

