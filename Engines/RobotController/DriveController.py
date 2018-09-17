from cozmo import util
from Settings.CozmoSettings import Settings
from Utils.InstanceManager import InstanceManager
from Engines.RobotController.RobotStatusController import RobotStatusController


class DriveController:
    robot = None

    def __init__(self):
        self.robot = InstanceManager.get_instance("Robot")

    def go(self):
        """
        Start driving straight
        """
        if Settings.cozmo_enable_drive:
            self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)

    def turn_next_left(self):
        RobotStatusController.is_at_crossing = True
        #self.robot.stop_all_motors()
        #self.robot.drive_straight(util.distance_mm(80), util.speed_mmps(Settings.cozmo_drive_speed)).wait_for_completed()
        #self.robot.turn_in_place(util.degrees(-90)).wait_for_completed()
        RobotStatusController.is_at_crossing = False

    def turn_next_right(self):
        RobotStatusController.is_at_crossing = True
        #self.robot.stop_all_motors()
        #self.robot.drive_straight(util.distance_mm(80), util.speed_mmps(Settings.cozmo_drive_speed)).wait_for_completed()
        #self.robot.turn_in_place(util.degrees(90)).wait_for_completed()
        RobotStatusController.is_at_crossing = False

    def move_next_straight(self):
        RobotStatusController.is_at_crossing = True
        #self.robot.stop_all_motors()
        #self.robot.drive_straight(util.distance_mm(100),
        #                          util.speed_mmps(Settings.cozmo_drive_speed)).wait_for_completed()
        RobotStatusController.is_at_crossing = False

    def correct(self, correction_value):
        """
            Correct path by turning left or right
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
