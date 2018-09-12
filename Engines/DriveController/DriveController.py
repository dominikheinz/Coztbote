from Settings.CozmoSettings import Settings
from Utils.InstanceManager import InstanceManager


class DriveController:
    robot = None

    def __init__(self):
        self.robot = InstanceManager.get_instance("Robot")

    def go(self):
        if Settings.cozmo_enable_drive:
            self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)

    def correct(self, correction_value):
        if Settings.cozmo_enable_drive:
            if correction_value > 0:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed,
                                              Settings.cozmo_drive_speed * (1 - abs(correction_value)))
            elif correction_value < 0:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed * (1 - abs(correction_value)),
                                              Settings.cozmo_drive_speed)
            else:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)
