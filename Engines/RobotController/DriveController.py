from cozmo import util
import datetime
from Utils import TimingUtils
from Settings.CozmoSettings import Settings
from Utils.InstanceManager import InstanceManager
from Engines.RobotController.RobotStatusController import RobotStatusController


class DriveController:
    robot = None

    def __init__(self):
        self.robot = InstanceManager.get_instance("Robot")

    # ToDo add stop method
    def start(self):
        """
        Start driving straight
        enable_drive is a static variable, taken from the Settings file
        where as allow_driving is being changed constantly while running
        """
        if Settings.cozmo_enable_drive:
            self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)

    def crossing_turn_right(self):
        RobotStatusController.is_at_crossing = True

        # Stop all driving behavior
        self.stop_autonomous_behaviour()

        # Approach the crossing
        self.robot.drive_straight(util.distance_mm(Settings.cozmo_crossing_approach_distance),
                                  util.speed_mmps(Settings.cozmo_drive_speed), should_play_anim=False)

        # Define turn method for later callback
        def turn(robot):
            robot.turn_in_place(util.degrees(90), util.degrees(180))

            def restart():
                RobotStatusController.is_at_crossing = False
                self.continue_autonomous_behaviour()

            TimingUtils.run_function_after(500 + 100, restart)

        drive_duration = ((Settings.cozmo_crossing_approach_distance / Settings.cozmo_drive_speed) * 1000) + 100
        # Run the previously defined turn method in drive_duration milliseconds
        TimingUtils.run_function_after(drive_duration, turn, self.robot)

    def crossing_turn_left(self):
        RobotStatusController.is_at_crossing = True

        # Stop all driving behavior
        self.stop_autonomous_behaviour()

        # Approach the crossing
        self.robot.drive_straight(util.distance_mm(Settings.cozmo_crossing_approach_distance),
                                  util.speed_mmps(Settings.cozmo_drive_speed), should_play_anim=False)

        # Define turn method for later callback
        def turn(robot):
            robot.turn_in_place(util.degrees(90), util.degrees(180))

            def restart():
                RobotStatusController.is_at_crossing = False
                self.continue_autonomous_behaviour()

            TimingUtils.run_function_after(500 + 100, restart)

        drive_duration = ((Settings.cozmo_crossing_approach_distance / Settings.cozmo_drive_speed) * 1000) + 100
        # Run the previously defined turn method in drive_duration milliseconds
        TimingUtils.run_function_after(drive_duration, turn, self.robot)

    def crossing_go_straight(self):
        RobotStatusController.is_at_crossing = True

        # Stop all driving behavior
        self.stop_autonomous_behaviour()

        # Approach the crossing
        self.robot.drive_straight(util.distance_mm(Settings.cozmo_crossing_approach_distance),
                                  util.speed_mmps(Settings.cozmo_drive_speed), should_play_anim=False)

        # Define restart method for later callback
        def restart():
            RobotStatusController.is_at_crossing = False
            self.continue_autonomous_behaviour()

        drive_duration = ((Settings.cozmo_crossing_approach_distance / Settings.cozmo_drive_speed) * 1000) + 10
        # Run the previously defined turn method in drive_duration milliseconds
        TimingUtils.run_function_after(drive_duration, restart)

    def stop_autonomous_behaviour(self):
        RobotStatusController.disable_autonomous_behavior = True
        self.robot.drive_wheel_motors(0, 0)
        self.robot.stop_all_motors()

    def continue_autonomous_behaviour(self):
        RobotStatusController.disable_autonomous_behavior = False
        self.start()

    def correct(self, correction_value):
        """
        Correct path by turning left or right
        enable_drive is a static variable, taken from the Settings file
        where as allow_driving is being changed constantly while running
        :param correction_value: Value between [-1..1], negative values meaning correct to the left,
        positive values to the right. The closer the value is to 0, the slighter it corrects.
        :type correction_value: float
        """
        if Settings.cozmo_enable_drive:
            if correction_value > 0:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed,
                                              Settings.cozmo_drive_speed * (1 - abs(correction_value)))
            elif correction_value < 0:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed * (1 - abs(correction_value)),
                                              Settings.cozmo_drive_speed)
            else:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)
