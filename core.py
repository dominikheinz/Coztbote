import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

def DriveInSquare(robot: cozmo.robot.Robot):
   while True:
       robot.drive_straight(distance_mm(200), speed_mmps(150), False, False, 0).wait_for_completed()
       robot.turn_in_place(cozmo.util.degrees(92), False, 0, angle_tolerance=degrees(0)).wait_for_completed()


cozmo.run_program(DriveInSquare)