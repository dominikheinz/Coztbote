from Settings.CozmoSettings import Settings


class DriveController:
    robot = None

    def __init__(self, robot):
        self.robot = robot

    def go(self):
        self.robot.drive_wheel_motors(Settings.cozmo_dive_speed, Settings.cozmo_dive_speed)

    def correct(self, correction_value):
        if correction_value > 0:
            self.robot.drive_wheel_motors(Settings.cozmo_dive_speed * 0.7, 0)
        elif correction_value < 0:
            self.robot.drive_wheel_motors(0, Settings.cozmo_dive_speed * 0.7)
        else:
            self.robot.drive_wheel_motors(Settings.cozmo_dive_speed, Settings.cozmo_dive_speed)
