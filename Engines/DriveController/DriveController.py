from Settings.CozmoSettings import Settings


class DriveController:
    robot = None

    def __init__(self, robot):
        self.robot = robot

    def go(self):
        self.robot.drive_wheel_motors(Settings.cozmo_dive_speed, Settings.cozmo_dive_speed)
        pass

    def correct(self, correction_value):
        if correction_value > 0:
            self.robot.drive_wheel_motors(Settings.cozmo_turn_speed_fast_wheel, Settings.cozmo_turn_speed_slow_wheel)
        elif correction_value < 0:
            self.robot.drive_wheel_motors(Settings.cozmo_turn_speed_slow_wheel, Settings.cozmo_turn_speed_fast_wheel)
        else:
            self.robot.drive_wheel_motors(Settings.cozmo_dive_speed, Settings.cozmo_dive_speed)
        pass
