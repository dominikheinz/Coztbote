from Controller.RobotStatusController import RobotStatusController
from Utils.InstanceManager import InstanceManager
from Engines.Navigation.TrackLoader import TrackLoader


class Navigator:
    current_track = None
    route_turn_index = 0
    route_is_reversed = False
    current_start = 0
    current_end = 0

    @staticmethod
    def set_route(start_point, end_point):
        """
        :param start_point: The start_point of the route
        :param end_point: The end_point of the route
        """
        print("Set route", str(start_point), str(end_point))
        Navigator.route_turn_index = 0
        Navigator.current_start = start_point
        Navigator.current_end = end_point
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

    @staticmethod
    def set_route_first_house():
        print("Go to first house", str(Navigator.current_end))
        Navigator.set_route(0, 1)

    @staticmethod
    def set_route_packet_station():
        Navigator.set_route(Navigator.current_end, 0)

    @staticmethod
    def set_route_next_house():
        print("Go to next house", str(Navigator.current_end))
        try:
            Navigator.set_route(Navigator.current_end, Navigator.current_end + 1)
        except ValueError:
            RobotStatusController.cube_undeliverable = True
            Navigator.current_end -= 1
            Navigator.set_route_packet_station()
