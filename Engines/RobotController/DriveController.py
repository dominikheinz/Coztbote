from Settings.CozmoSettings import Settings
from Utils.InstanceManager import InstanceManager


class DriveController:
    robot = None
    allow_driving = True

    def __init__(self):
        self.robot = InstanceManager.get_instance("Robot")

    def go(self):
        """
        Start driving straight
        """
        if Settings.cozmo_enable_drive and self.allow_driving:
            self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)
        else:
            self.robot.drive_wheel_motors(0,0)

    def correct(self, correction_value):
        """
        Correct path by turning left or right
        :param correction_value: Value between [-1..1], negative values meaning correct to the left,
        positive values to the right. The closer the value is to 0, the slighter it corrects.
        :type correction_value: float
        """
        if Settings.cozmo_enable_drive and self.allow_driving:
            if correction_value > 0:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed,
                                              Settings.cozmo_drive_speed * (1 - abs(correction_value)))
            elif correction_value < 0:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed * (1 - abs(correction_value)),
                                              Settings.cozmo_drive_speed)
            else:
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)
        else:
            self.robot.drive_wheel_motors(0,0)