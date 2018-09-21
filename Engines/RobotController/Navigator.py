from Engines.LaneTracking.CrossingType import CrossingType
from Utils.InstanceManager import InstanceManager
from Engines.RobotController import RobotStatusController
from Engines.RobotController.TrackLoader import TrackLoader
from Utils.PreviewUtils import PreviewUtils


class Navigator:
    current_track = None
    route_turn_index = 0
    route_is_reversed = False

    def handle_crossing(self, crossing_type):
        if crossing_type is not None:
            Navigator.navigate()

        """
        if crossing_type == CrossingType.Crossing:
            self.drive_controller.crossing_go_straight()  # ToDo Change Direction
        elif crossing_type == CrossingType.T_Crossing:
            self.drive_controller.crossing_turn_left()  # ToDo Change Direction
        elif crossing_type == CrossingType.Right_T_Crossing:
            self.drive_controller.crossing_turn_right()  # ToDo Change Direction
        elif crossing_type == CrossingType.Left_T_Crossing:
            self.drive_controller.crossing_turn_left()  # ToDo Change Direction
        else:
            RobotStatusController.is_at_crossing = False
            self.drive_controller.start()
        """

    @staticmethod
    def set_route(start_point, end_point):
        """
        :param start_point: The start_point of the route
        :param end_point: The end_point of the route
        """
        Navigator.route_turn_index = 0
        Navigator.current_track = TrackLoader.load_track(start_point, end_point)

    @staticmethod
    def reverse_route():
        reversed_route = Navigator.current_track

        reversed_route.reverse()

        for i in range(0, len(reversed_route)):
            if reversed_route[i] == 'L':
                reversed_route[i] = 'R'
            elif reversed_route[i] == 'R':
                reversed_route[i] = 'L'

        Navigator.route_turn_index = 0
        Navigator.route_is_reversed = False

    @staticmethod
    def navigate():
        """
        Navigates the robot from start to endpoint
        :return: True if robot has arrived at endpoint, false otherwise
        """

        drive_controller = InstanceManager.get_instance("DriveController")

        # If track is none it has not been loaded yet
        if Navigator.current_track is None:
            raise Exception("Route not set")

        # Execute next turn
        if Navigator.current_track[Navigator.route_turn_index] == "L":
            drive_controller.crossing_turn_left()
        elif Navigator.current_track[Navigator.route_turn_index] == "R":
            drive_controller.crossing_turn_right()
        elif Navigator.current_track[Navigator.route_turn_index] == "S":
            drive_controller.crossing_go_straight()
        else:
            raise Exception("Invalid turn operation")

        # Update route turn index
        Navigator.route_turn_index += 1

        # All track turns are completed, we have arrived at end point
        # Reverse route to drive back
        if (Navigator.route_turn_index >= len(Navigator.current_track) and not Navigator.route_is_reversed) or \
                (Navigator.route_turn_index < 0 and Navigator.route_is_reversed):
            Navigator.reverse_route()

        # Return false if route was not yet completed
        return False
