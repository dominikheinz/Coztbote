import asyncio

import cozmo
from cozmo.util import degrees, Angle
from Settings.CozmoSettings import Settings
from Engines.RobotController.RobotStatusController import RobotStatusController

"""
Used for observing cubes and facing and comparing pairs of faces and 
cubes that have been defined as matching by dictionary
"""


class CubeFacePairing:

    @staticmethod
    def initialize(robot: cozmo.robot.Robot):
        """
           Makes robot ready for duty. Shows battery, and sets head tilt and forklift to neutral
           """
        print("INITIALIZE: Raising head and lowering forklift at the same time!")
        action_lower_head = robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE / 4,
                                                 in_parallel=True)  # saving as actions and waiting for complete
        action_set_forklift = robot.set_lift_height(0, 5, 10, 1, True, 0)  # so the actions can be performed parallel
        action_lower_head.wait_for_completed()
        action_set_forklift.wait_for_completed()

    @staticmethod
    def wait_for_face(robot: cozmo.robot.Robot, perceivedFaces):
        perceivedFaces.append(robot.wait_for(
            cozmo.faces.EvtFaceAppeared).face)  # Saves an Instance of Face contained by the face appeared Event
        print("Name of the person: " + perceivedFaces[0].name)
        return perceivedFaces

    @staticmethod
    def compare_cube_and_face(robot: cozmo.robot.Robot, name, idFace, idCube, face):
        """
            Checks if face is matching the Cube
            :param name: name of the face that has been observed
            :param idFace: id of the face that has been observed
            :param idCube: id of the cube that has been observed
            :param face: the face itself that has been observed
            :return: bool that determines whether the given pair is matching
            """
        robot.turn_towards_face(face).wait_for_completed()

        face_matching = False
        if not name == '':  # An empty string is in this case shown as a char, which fails the comparison
            if idFace == idCube:
                print("MATCH")
                action_lift = robot.set_lift_height(0, 5, 10, 1, True, 0)
                action_speak = robot.say_text(Settings.tts_packet_deliverd + name, in_parallel=True,
                                              use_cozmo_voice=False)
                action_lift.wait_for_completed()  # Raising Forks if correct
                action_speak.wait_for_completed()
                face_matching = True
                RobotStatusController.is_holding_cube = True
            else:
                print("NO Match but recognized")
                RobotStatusController.face_recognized_but_not_matching = True

        else:
            print("Face not recognized")
        return face_matching

    @staticmethod
    def look_for_faces(robot: cozmo.robot.Robot):
        print("Setting Head angle for face detection..")
        robot.set_head_angle(Angle(0.9), 100).wait_for_completed()
        face = None
        while not face:
            try:
                face = robot.world.wait_for_observed_face(timeout=5)
            except asyncio.TimeoutError:
                print(asyncio.TimeoutError)
                face = []
                break

        return face
