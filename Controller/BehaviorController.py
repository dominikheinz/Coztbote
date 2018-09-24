import asyncio

from Engines.Navigation.Navigator import Navigator
from Engines.SignHandler.SignHandler import SignHandler
from Utils.InstanceManager import InstanceManager
import cozmo
from Settings.CozmoSettings import Settings
from cozmo.util import degrees, distance_mm, speed_mmps, Angle
from Controller.RobotStatusController import RobotStatusController
from Utils.PreviewUtils import PreviewUtils


class BehaviorController:
    perceived_cubes = []
    perceived_faces = []
    face_recognized_but_not_matching = False

    def __init__(self):
        self.robot = InstanceManager.get_instance("Robot")
        self.drive_controller = InstanceManager.get_instance("DriveController")

    def move_lift_up(self):
        self.robot.set_lift_height(height=1.0, in_parallel=True)

    def move_lift_middle(self):
        self.robot.set_lift_height(height=0.4, in_parallel=True)

    def move_lift_down(self):
        self.robot.set_lift_height(height=0.0, in_parallel=True)

    def say_text(self, text):
        self.robot.say_text(text, in_parallel=True, use_cozmo_voice=False, duration_scalar=0.5).wait_for_completed()

    def move_head_up(self):
        self.robot.set_head_angle(Angle(0.9), in_parallel=True)

    def move_head_down(self):
        self.robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE + cozmo.util.degrees(4), in_parallel=True)

    def move_head_middle(self):
        self.robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE / 4, in_parallel=True)

    def run_packet_station_behavior(self):

        if not RobotStatusController.is_in_packet_station:
            print("Enter packetstation")
            PreviewUtils.show_preview_text("Picking up package")
            RobotStatusController.is_in_packet_station = True
            Settings.cozmo_drive_speed = 35
            self.drive_controller.stop_autonomous_behavior()

            if RobotStatusController.cube_undeliverable:
                self.say_text("Ich konnte den Empfänger leider nicht finden.")
                self._place_undeliverable_package()
                RobotStatusController.is_holding_cube = False

            self.go_to_cube_searching_pose()

            self.perceived_cubes = []
            self.perceived_faces = []

            try:
                self.perceived_cubes.append(self._search_for_cube(timeout=30))
                print("Cube found:", self.perceived_cubes[0].descriptive_name)

                self._pickup_cube_until_successful(self.perceived_cubes[0])

                self.robot.turn_in_place(degrees(-90), in_parallel=False, num_retries=1).wait_for_completed()

                self.move_head_up()
                self.robot.wait_for_all_actions_completed()
                self.move_head_down()
                self.robot.wait_for_all_actions_completed()

                RobotStatusController.holding_cube_id = self.perceived_cubes[0].object_id

                self.robot.drive_straight(distance_mm(50), speed_mmps(20), should_play_anim=False,
                                          in_parallel=False, num_retries=3).wait_for_completed()

            except IndexError:
                print("No cube found in array!")

            RobotStatusController.cube_undeliverable = False
            Navigator.set_route_first_house()

            self.drive_controller.continue_autonomous_behavior()

        else:
            RobotStatusController.is_in_packet_station = False
            Settings.cozmo_drive_speed = 50
            RobotStatusController.is_holding_cube = True
            SignHandler.trigger_sign_detection_cooldown()
            print("Leaving packetstation")

    def run_face_matching_behavior(self):

        if RobotStatusController.is_holding_cube:
            PreviewUtils.show_preview_text("Checking house")

            self.drive_controller.stop_autonomous_behavior()
            self.go_to_face_recognition_pose()

            self._cube_face_pairing()
            self._reinitialize_for_lanetracking()
            self.drive_controller.continue_autonomous_behavior()
        else:
            SignHandler.trigger_sign_detection_cooldown()
            self.drive_controller.turn_around()

    def _pickup_cube_until_successful(self, perceived_cube):
        pickup_action = self.robot.pickup_object(perceived_cube, use_pre_dock_pose=False, in_parallel=False,
                                                 num_retries=3)
        pickup_action.wait_for_completed()

        while pickup_action.has_failed:
            print("Picking up failed")
            self.robot.drive_straight(distance_mm(-50), speed_mmps(20), should_play_anim=False,
                                      in_parallel=False, num_retries=3).wait_for_completed()
            self.perceived_cubes = []
            self.perceived_cubes.append(self._search_for_cube(timeout=30))
            pickup_action = self.robot.pickup_object(perceived_cube, False, False, 3)
            pickup_action.wait_for_completed()
            print(pickup_action)

    def _place_undeliverable_package(self):
        self.robot.drive_straight(distance_mm(50), speed_mmps(Settings.cozmo_drive_speed), should_play_anim=True,
                                  in_parallel=False, num_retries=3).wait_for_completed()
        self.robot.turn_in_place(degrees(-90), in_parallel=False, num_retries=1).wait_for_completed()
        self.robot.drive_straight(distance_mm(100), speed_mmps(Settings.cozmo_drive_speed), should_play_anim=True,
                                  in_parallel=False, num_retries=3).wait_for_completed()

        # Place cube on ground
        self.robot.place_object_on_ground_here(self.perceived_cubes[0],
                                               in_parallel=False).wait_for_completed()

        self.robot.drive_straight(distance_mm(-100), speed_mmps(Settings.cozmo_drive_speed), should_play_anim=True,
                                  in_parallel=False, num_retries=3).wait_for_completed()
        self.robot.turn_in_place(degrees(170), in_parallel=False, num_retries=1).wait_for_completed()

    def _search_for_cube(self, timeout):
        """
               Waits for a Cube to appear and return its data
               :param timeout: how long the robot will wait for an observable cube until it stops
               :return: the cube that has been spotted
               """
        look_around = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        perceived_cubes = self.robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube,
                                                                          timeout=timeout)
        look_around.stop()
        print("Stopped looking around")
        return perceived_cubes[0]

    def go_to_lane_tracking_pose(self):
        self.move_lift_up()
        self.move_head_down()
        self.robot.wait_for_all_actions_completed()

    def go_to_cube_searching_pose(self):
        self.move_lift_down()
        self.move_head_middle()
        self.robot.wait_for_all_actions_completed()

    def go_to_face_recognition_pose(self):
        """
        Makes robot ready for duty. Sets head tilt and forklift to neutral
        """
        self.move_lift_middle()
        self.move_head_up()
        self.robot.wait_for_all_actions_completed()

    def _wait_for_face(self, perceived_faces):
        # Saves an Instance of Face contained by the face appeared Event
        perceived_faces.append(self.robot.wait_for(cozmo.faces.EvtFaceAppeared).face)
        print("Name of the person: " + perceived_faces[0].name)
        return perceived_faces

    def _is_cube_matching_face(self, name, face_id, cube_id, face):
        """
            Checks if face is matching the Cube
            :param name: name of the face that has been observed
            :param face_id: id of the face that has been observed
            :param cube_id: id of the cube that has been observed
            :param face: the face itself that has been observed
            :return: bool that determines whether the given pair is matching
            """
        self.robot.turn_towards_face(face).wait_for_completed()

        face_matching = False
        if not name == '':  # An empty string is in this case shown as a char, which fails the comparison
            if face_id == cube_id:
                print("Face matches cube!")
                self.move_lift_down()
                self.say_text(Settings.tts_packet_delivered + name)
                self.robot.wait_for_all_actions_completed()

                face_matching = True
                RobotStatusController.is_holding_cube = False

            else:
                print("Face does not match cube, but recognized")
                self.face_recognized_but_not_matching = True
        else:
            print("Face not recognized")
        return face_matching

    def _look_for_faces(self):
        self.go_to_face_recognition_pose()
        face = None
        while not face:
            try:
                face = self.robot.world.wait_for_observed_face(timeout=5)
            except asyncio.TimeoutError:
                print(asyncio.TimeoutError)
                face = []
                break
        print("Value of face var:", face)
        return face

    def _cube_face_pairing(self):
        matching_counter = 0
        cube_is_matching_face = False
        self.face_recognized_but_not_matching = False
        while matching_counter < 10 and not cube_is_matching_face:
            self.perceived_faces = []
            self.perceived_faces.append(self._look_for_faces())

            try:
                owner_id = Settings.owner_dict[self.perceived_faces[0].name]
                cube_is_matching_face = self._is_cube_matching_face(self.perceived_faces[0].name, owner_id,
                                                                    self.perceived_cubes[0].object_id,
                                                                    self.perceived_faces[0])
            except AttributeError as e:
                print("Owner error:", self.perceived_faces)
                print(e)

            if self.face_recognized_but_not_matching:
                break

            matching_counter += 1

        if cube_is_matching_face:
            self.robot.place_object_on_ground_here(self.perceived_cubes[0],
                                                   in_parallel=False).wait_for_completed()
            RobotStatusController.is_holding_cube = False
            Navigator.set_route_packet_station()
        else:
            if self.face_recognized_but_not_matching:
                self.say_text(Settings.tts_wrong_house_personal + self.perceived_faces[0].name)
            else:
                self.say_text(Settings.tts_wrong_house)
            Navigator.set_route_next_house()
        self.perceived_faces = []

    def _reinitialize_for_lanetracking(self):
        self.drive_controller.stop_autonomous_behavior()
        self.go_to_lane_tracking_pose()
        self.robot.drive_straight(distance_mm(-30), speed_mmps(20), False, False, 3).wait_for_completed()
        self.robot.turn_in_place(degrees(180)).wait_for_completed()
        SignHandler.trigger_sign_detection_cooldown()
