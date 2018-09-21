import cozmo

from cozmo.util import degrees, distance_mm, speed_mmps, Angle
from Engines.ImageRecognition.CubeFacePairing import CubeFacePairing

def packet_station(robot: cozmo.robot.Robot):
    packet_station_behavior(robot)


def packet_station_behavior(robot):
    CubeFacePairing.initialize(robot)
    perceived_cubes = []
    try:
        cube = CubeFacePairing.search_for_cube(robot, 10)
        print("Cube found")
        perceived_cubes.append(cube)
        print("Cube observed: " + cube.descriptive_name)
        robot.pickup_object(perceived_cubes[0], False, False, 10).wait_for_completed()
        robot.turn_in_place(degrees(180), False, 1).wait_for_completed()

    except IndexError:
        print("No cube found in array!")


cozmo.run_program(packet_station)