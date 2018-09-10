import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.util import degrees, distance_mm, Speed
from cozmo.faces import Face

def cube_to_face(robot: cozmo.robot.Robot):

    cube0 = robot.world.get_light_cube(LightCube1Id)  # looks like a paperclip
    cube1 = robot.world.get_light_cube(LightCube2Id)  # looks like a lamp / heart
    cube2 = robot.world.get_light_cube(LightCube3Id)  # looks like the letters 'ab' over 'T'

    key_value = {"Eric": 0, "Fabian hehe": 1, "Gero": 2}

    while True:
        initialize(robot)
        #perceivedCubes = []

        perceivedCubes = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=20)
        print("Cube observed: " + perceivedCubes[0].descriptive_name)

        perceivedFaces = []

        perceivedFaces = wait_for_cube(robot,perceivedFaces)

        check_cube_for_face(robot,perceivedFaces[0].name ,key_value[perceivedFaces[0].name],perceivedCubes[0].object_id)

        print("FINISHED, next run!")

#Used to set Cozmo to default position. Fork down and Head up
def initialize(robot: cozmo.robot.Robot):
    print("Raising head and lowering forklift at the same time!")
    action_lower_head = robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE / 4, in_parallel=True)
    action_set_liftfork = robot.set_lift_height(0, 5, 10, 1, True, 0)
    action_lower_head.wait_for_completed()
    action_set_liftfork.wait_for_completed()

#Sets Cozmo in waiting state until Cube appears
def wait_for_cube(robot: cozmo.robot.Robot, perceivedFaces):
    perceivedFaces.append(robot.wait_for(
        cozmo.faces.EvtFaceAppeared).face)  # Saves an Instance of Face contained by the face appeared Event
    print("Name of the person: " + perceivedFaces[0].name)
    return perceivedFaces

#Sets Cozmo in waiting state until face "appears" and checks if face is matching the Cube
def check_cube_for_face(robot: cozmo.robot.Robot,name, idFace, idCube):
    if not name == '':
        if idFace == idCube:
            print("MATCH")
            robot.set_lift_height(1, 5, 10, 1, False, 0).wait_for_completed()
        else:
            robot.say_text("ES PASST NICHT!!").wait_for_completed()

cozmo.run_program(cube_to_face)

##
#if not perceivedFaces[0].name == '':
#    if key_value[perceivedFaces[0].name] == perceivedCubes[0].object_id:
#        print("MATCH")
#        robot.set_lift_height(1, 5, 10, 1, False, 0).wait_for_completed()
#    else:
#        robot.say_text("ES PASST NICHT!!").wait_for_completed()