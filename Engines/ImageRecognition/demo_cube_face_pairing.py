import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Angle

from Engines.ImageRecognition.CubeFacePairing import CubeFacePairing


# Scans a cube, then a face. Determines whether or not the cube belongs to the face according to a dictionary
# Then proceeds to deliver the cube to the person whose face is matching in the dictionary
def demo_haul_cube_to_face(robot: cozmo.robot.Robot):
    owner_dict = {"Eric": 0, "Fabian hehe": 1, "Fabian": 1, "Gero": 2, '': -1}  # -1 as error code for unknown access

    while True:
        CubeFacePairing.initialize(robot)

        perceived_cubes = []
        perceived_faces = []

        try:
            cube = CubeFacePairing.search_for_cube(robot, 10)
            print("Cube found")
            perceived_cubes.append(cube)
            print("Cube observed: " + cube.descriptive_name)

        except IndexError:
            print("No cube found in array!")
            continue

        print("Picking up Cube")

        robot.pickup_object(perceived_cubes[0], False, False, 10).wait_for_completed()

        robot.set_lift_height(0.4).wait_for_completed()

        perceived_faces.append(CubeFacePairing.look_for_faces(robot))
        is_matching = CubeFacePairing.compare_cube_and_face(robot, perceived_faces[0].name,
                                                            owner_dict[perceived_faces[0].name],
                                                            perceived_cubes[0].object_id, perceived_faces[0])
        while not is_matching:
            perceived_faces = []
            # robot.turn_in_place(degrees(90)).wait_for_completed()
            perceived_faces.append(CubeFacePairing.look_for_faces(robot))
            is_matching = CubeFacePairing.compare_cube_and_face(robot, perceived_faces[0].name,
                                                                owner_dict[perceived_faces[0].name],
                                                                perceived_cubes[0].object_id, perceived_faces[0])

        robot.drive_straight(distance_mm(150), speed_mmps(50)).wait_for_completed()
        action_speak = robot.say_text("Hier ist dein Würfel " + perceived_faces[0].name, in_parallel=True,
                                      use_cozmo_voice=False)
        action_drop = robot.place_object_on_ground_here(perceived_cubes[0], in_parallel=True)
        action_speak.wait_for_completed()
        action_drop.wait_for_completed()

        print("FINISHED, next run!")


cozmo.run_program(demo_haul_cube_to_face)
