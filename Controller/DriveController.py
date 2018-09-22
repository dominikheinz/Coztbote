from cozmo import util
from Utils import TimingUtils
from Settings.CozmoSettings import Settings
from Utils.InstanceManager import InstanceManager
from Controller.RobotStatusController import RobotStatusController


# noinspection PyPep8
class DriveController:
    robot = None

    def __init__(self):
        self.robot = InstanceManager.get_instance("Robot")

    def start(self):
        """
        Start driving straight
        """
        if not Settings.disable_driving:
            self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)

    def crossing_turn_right(self):
        """
        Run all behaviour associated with turning right at a crossing
        """
        if not Settings.disable_driving:
            RobotStatusController.is_at_crossing = True

            # Stop all driving behavior
            self.stop_autonomous_behaviour()

            # Approach the crossing
            drive_action = self.robot.drive_straight(util.distance_mm(Settings.crossing_approach_distance),
                                                     util.speed_mmps(Settings.cozmo_drive_speed), should_play_anim=False)

            # Calculate how long the approaching will take
            drive_duration = ((Settings.crossing_approach_distance / Settings.cozmo_drive_speed) * 1000)

            # Run the previously defined turn method in drive_duration milliseconds
            TimingUtils.run_function_after_if_action_finished(drive_duration, drive_action, self._turn_at_crossing, -90)

    def crossing_turn_left(self):
        """
        Run all behaviour associated with turning left at a crossing
        """
        if not Settings.disable_driving:
            RobotStatusController.is_at_crossing = True

            # Stop all driving behavior
            self.stop_autonomous_behaviour()

            # Approach the crossing
            drive_action = self.robot.drive_straight(util.distance_mm(Settings.crossing_approach_distance),
                                                     util.speed_mmps(Settings.cozmo_drive_speed), should_play_anim=False)

            # Calculate how long the approaching will take
            drive_duration = ((Settings.crossing_approach_distance / Settings.cozmo_drive_speed) * 1000)

            # Run the previously defined turn method in drive_duration milliseconds
            TimingUtils.run_function_after_if_action_finished(drive_duration, drive_action, self._turn_at_crossing, 90)

    def crossing_go_straight(self):
        """
        Run all behaviour associated with going straight at a crossing
        """
        if not Settings.disable_driving:
            RobotStatusController.is_at_crossing = True

            # Stop all driving behavior
            self.stop_autonomous_behaviour()

            # Approach the crossing
            drive_action = self.robot.drive_straight(util.distance_mm(Settings.crossing_approach_distance),
                                                     util.speed_mmps(Settings.cozmo_drive_speed), should_play_anim=False)

            # Calculate how long the approaching will take
            drive_duration = ((Settings.crossing_approach_distance / Settings.cozmo_drive_speed) * 1000)

            # Run the previously defined turn method in drive_duration milliseconds
            TimingUtils.run_function_after_if_action_finished(drive_duration, drive_action, self._continue_after_crossing)

    def _turn_at_crossing(self, degrees):
        """
        Turn in place when directly on top of a crossing
        :param degrees: How many degrees to turn
        """
        turn_action = self.robot.turn_in_place(util.degrees(degrees),
                                               speed=util.degrees(Settings.cozmo_turn_speed_degrees_per_second))

        turn_duration = (degrees / Settings.cozmo_turn_speed_degrees_per_second) * 1000
        TimingUtils.run_function_after_if_action_finished(turn_duration, turn_action, self._continue_after_crossing)

    def _continue_after_crossing(self):
        """
        Restart normal behaviour after crossing has been passed
        """
        RobotStatusController.is_at_crossing = False
        self.continue_autonomous_behaviour()

    def stop_autonomous_behaviour(self):
        """
        Stop all autonomous behaviour like lane correction, crossing detection and sign detection.
        Cozmo will stop driving.
        """
        RobotStatusController.disable_autonomous_behavior = True
        self.robot.drive_wheel_motors(0, 0)
        self.robot.stop_all_motors()

    def continue_autonomous_behaviour(self):
        """
        Continue all autonomous behaviour like lane correction, crossing detection and sign detection.
        Cozmo will start driving.
        """
        RobotStatusController.disable_autonomous_behavior = False
        self.robot.stop_all_motors()
        self.start()

    def turn_around(self):
        self.stop_autonomous_behaviour()
        turn_action = self.robot.turn_in_place(util.degrees(180), speed=util.degrees(180))
        turn_duration = (180 / Settings.cozmo_turn_speed_degrees_per_second) * 1000
        TimingUtils.run_function_after_if_action_finished(turn_duration, turn_action,
                                                          self.continue_autonomous_behaviour)

    def correct(self, correction_value):
        """
        Correct path by turning left or right
        :param correction_value: Value between [-1..1], negative values meaning correct to the left,
        positive values to the right. The closer the value is to 0, the slighter it corrects.
        :type correction_value: float
        """
        if not Settings.disable_driving:
            if correction_value > 0:
                # Correct to the right
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed,
                                              Settings.cozmo_drive_speed * (1 - abs(correction_value)))
            elif correction_value < 0:
                # Correct to the left
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed * (1 - abs(correction_value)),
                                              Settings.cozmo_drive_speed)
            else:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)

    def correct_in_place(self, correction_value):
        """
        Correct facing direction by rotating left or right in place
        :param correction_value: Value between [-1..1], negative values meaning correct to the left,
        positive values to the right. The closer the value is to 0, the slighter it corrects.
        :type correction_value: float
        """
        if not Settings.disable_driving:
            if correction_value > 0:
                # Rotate to the right
                self.robot.drive_wheel_motors((Settings.cozmo_drive_speed * abs(correction_value)),
                                              -(Settings.cozmo_drive_speed * abs(correction_value)))
            elif correction_value < 0:
                # Rotate to the left
                self.robot.drive_wheel_motors(-(Settings.cozmo_drive_speed * abs(correction_value)),
                                              (Settings.cozmo_drive_speed * abs(correction_value)))
            else:
                self.robot.drive_wheel_motors(0, 0)
