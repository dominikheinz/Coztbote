import cozmo
from cozmo.util import degrees, distance_mm, Speed
from Engines.PacketStation.CubeFacePairing import CubeFacePairing
from Engines.RobotController.RobotStatusController import RobotStatusController


def packet_station_behavior(robot):
    CubeFacePairing.initialize(robot)

    try:
        cube = search_for_cube(robot, 30)
        print("Cube found")
        RobotStatusController.perceived_cubes.append(cube)
        print("Cube observed: " + cube.descriptive_name)
        pickup_action = robot.pickup_object(RobotStatusController.perceived_cubes[0], False, False, 3)
        pickup_action.wait_for_completed()
        while pickup_action.has_failed:
            print("picking up failed")
            robot.drive_straight(distance_mm(-50), Speed(20), True, False, 3).wait_for_completed()
            pickup_action = robot.pickup_object(RobotStatusController.perceived_cubes[0], False, False,
                                                3)
            pickup_action.wait_for_completed()
        robot.turn_in_place(degrees(-90), False, 1).wait_for_completed()

    except IndexError:
        print("No cube found in array!")


def search_for_cube(robot: cozmo.robot.Robot, timeout):
    """
       Waits for a Cube to appear and return its data
       :param timeout: how long the robot will wait for an observable cube until it stops
       :return: the cube that has been spotted
       """
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    perceived_cube = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube,
                                                                timeout=timeout)
    look_around.stop()
    print("Stopped looking around")
    return perceived_cube[0]