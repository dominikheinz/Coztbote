from argparse import _AppendAction

import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.util import degrees, distance_mm, Speed

def deliver(robot: cozmo.robot.Robot):

    cube1 = robot.world.get_light_cube(LightCube1Id)  # looks like a paperclip
    cube2 = robot.world.get_light_cube(LightCube2Id)  # looks like a lamp / heart
    #cube3 = robot.world.get_light_cube(LightCube3Id)  # looks like the letters 'ab' over 'T'

    print("Raising head and lowering forklift!")
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE / 8).wait_for_completed()
    robot.set_lift_height(0, 5, 10, 1, False, 0).wait_for_completed()

    perceivedCubes = robot.world.wait_until_observe_num_objects(num=2, object_type=cozmo.objects.LightCube, timeout=20)
    print(len(perceivedCubes))

    print("objects detected!")

    print("going to first cube!")
    #robot.go_to_object(cube1, distance_mm(80.0)).wait_for_completed()


    print("Picking it up!")
    currentAction = robot.pickup_object(cube1, False, False, 3)
    currentAction.wait_for_completed()

    while currentAction.has_failed:
        print("Failed picking up cube1!")
        robot.drive_straight(distance_mm(-100), Speed(20), True, False, 3).wait_for_completed()
        currentAction = robot.pickup_object(cube1, False, False, 3)
        currentAction.wait_for_completed()

    print("Stacking the cubes!")

    if len(perceivedCubes) == 2:

        print("looking around!")
        #robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

        #currentBehaviour = robot.run_timed_behavior(cozmo.behavior.BehaviorTypes.StackBlocks, active_time=60)
        currentAction = robot.go_to_object(cube2, distance_mm(80.0)).wait_for_completed()

        currentcubes = 0
        while len(currentcubes) == 0:
            print("finding and moving towards failed, trying again!")
            currentcubes = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=60)
            robot.turn_in_place(degrees(40)).wait_for_completed()

            #robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)


        currentAction = robot.go_to_object(cube2, distance_mm(80.0)).wait_for_completed()

        currentAction = robot.place_on_object(cube2, False, False, 3)

        while currentAction.has_failed:
            print("stacking failed, retrying again!")
            currentAction = robot.place_on_object(cube2, False, False, 3)

        print("Now saying finishing line")
        robot.say_text("hee heee heeeee", voice_pitch=1, duration_scalar=0.1).wait_for_completed()
    else:
        robot.say_text("Das war wohl ein Schuss in den Ofen!").wait_for_completed()

cozmo.run_program(deliver)