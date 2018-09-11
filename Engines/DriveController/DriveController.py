from Settings.CozmoSettings import Settings


class DriveController:
    robot = None

    def __init__(self, robot):
        self.robot = robot

    def go(self):
        if Settings.cozmo_enable_drive:
            self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)

    def correct(self, correction_value):
        if Settings.cozmo_enable_drive:
            if correction_value > 0:
                print("Correction: Right", correction_value)
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed * (1-abs(correction_value)))
            elif correction_value < 0:
                print("Correction: Left", correction_value)
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed * (1-abs(correction_value)), Settings.cozmo_drive_speed)
            else:
                print("Correction: None")
                self.robot.drive_wheel_motors(Settings.cozmo_drive_speed, Settings.cozmo_drive_speed)
