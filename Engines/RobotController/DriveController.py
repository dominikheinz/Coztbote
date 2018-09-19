from cozmo import util
import datetime, cozmo
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
        """
        if Settings.cozmo_enable_drive:
            self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)

    def crossing_turn_left(self):
        RobotStatusController.is_at_crossing = True
        self.robot.stop_all_motors()
        self.robot.drive_straight(util.distance_mm(170), util.speed_mmps(Settings.cozmo_drive_speed), should_play_anim=False)
        RobotStatusController.crossing_turn_degrees = 90
        self.set_crossing_status(1)

    def crossing_turn_right(self):
        RobotStatusController.is_at_crossing = True
        self.robot.stop_all_motors()
        self.robot.drive_straight(util.distance_mm(170), util.speed_mmps(Settings.cozmo_drive_speed),
                                  should_play_anim=False)
        RobotStatusController.crossing_turn_degrees = -90
        self.set_crossing_status(1)

    def crossing_go_straight(self):
        RobotStatusController.is_at_crossing = True
        self.robot.stop_all_motors()
        self.robot.drive_straight(util.distance_mm(170), util.speed_mmps(Settings.cozmo_drive_speed),
                                  should_play_anim=False)
        RobotStatusController.crossing_turn_degrees = 0
        self.set_crossing_status(1)

    def correct(self, correction_value):
        """
            Correct path by turning left or right
            :param correction_value: Value between [-1..1], negative values meaning correct to the left,
            positive values to the right. The closer the value is to 0, the slighter it corrects.
            :type correction_value: float
            """
        print()
        if Settings.cozmo_enable_drive:
            if correction_value > 0:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed,
                                              Settings.cozmo_drive_speed * (1 - abs(correction_value)))
            elif correction_value < 0:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed * (1 - abs(correction_value)),
                                              Settings.cozmo_drive_speed)
            else:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)

    def check_crossing_status_cooldown(self):
        """
        Checks last timestamp if time delta is exceeded, to block or
        unblock sign_recognition_cooldown boolean
        :param time_sign_seen: time when sign is seen
        :param disable_cooldown: bool to disable cooldown functionality
        """
        # Checks if time interval is big enough to unlock the sign_recognition_cooldown
        if RobotStatusController.crossing_status == 1:
            if RobotStatusController.crossing_status_change_timestamp < datetime.datetime.now() - datetime.timedelta(
                    milliseconds=2500):
                self.robot.stop_all_motors()
                if RobotStatusController.crossing_turn_degrees != 0:
                    self.robot.turn_in_place(util.degrees(RobotStatusController.crossing_turn_degrees))
                    self.set_crossing_status(2)
                else:
                    RobotStatusController.is_at_crossing = False
                    self.set_crossing_status(0)
        elif RobotStatusController.crossing_status == 2:
            if RobotStatusController.crossing_status_change_timestamp < datetime.datetime.now() - datetime.timedelta(
                    milliseconds=1000):
                RobotStatusController.is_at_crossing = False
                self.set_crossing_status(0)

    def set_crossing_status(self, new_status):
        RobotStatusController.crossing_status = new_status
        RobotStatusController.crossing_status_change_timestamp = datetime.datetime.now()
