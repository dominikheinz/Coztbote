from Settings.CozmoSettings import Settings
import cozmo
import datetime
from cozmo.util import degrees, distance_mm, Speed
from Utils.InstanceManager import InstanceManager
from Engines.RobotController.RobotStatusController import RobotStatusController
from Utils import TimingUtils
from Engines.PacketStation import PacketStation
from Engines.PacketStation.CubeFacePairing import CubeFacePairing

class SignHandler:

    RobotStatusController = None
    robot = None
    drive_controller = None

    def __init__(self):
        """
        Creating an instance of robot and getting the cooldown_time_ms from Settings.py
        """
        self.robot = InstanceManager.get_instance("Robot")
        self.lane_analyzer = InstanceManager.get_instance("CorrectionCalculator")
        self.drive_controller = InstanceManager.get_instance("DriveController")

    @staticmethod
    def trigger_sign_detection_cooldown():
        RobotStatusController.enable_sign_recognition = False

        def restart_detection():
            RobotStatusController.enable_sign_recognition = True

        TimingUtils.run_function_after(Settings.sign_detection_cooldown_time, restart_detection)

    def react_to_signs(self, sign_count):
        """
        Tells Cozmo what to do for every sign(amount of signs)
        :param sign_count: amount of spotted signs
        """
        if (sign_count % 2) == 1:
            # Handling for wrong identified signs, cause there als only even amount of signs
            print("Odd_Sign_Count_Error")

        elif sign_count == 4:
            # Handling four spotted signs

            self.drive_controller.stop_autonomous_behaviour()

            self.robot.stop_all_motors()
            self.robot.set_lift_height(0.4).wait_for_completed()
            RobotStatusController.perceived_faces.append(CubeFacePairing.look_for_faces(self.robot))
            is_matching = self.check_if_matching()
            self.search_for_faces_until_matching(is_matching)

            self.reinitialize_for_lanetracking()

            self.robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE + cozmo.util.degrees(4), in_parallel=False)
            self.drive_controller.continue_autonomous_behaviour()

        elif sign_count == 6:
            # Handling for six spotted signs
            SignHandler.trigger_sign_detection_cooldown()
            self.drive_controller.stop_autonomous_behaviour()
            turn_action = self.robot.turn_in_place(degrees(180), speed=degrees(180))
            turn_duration = (180 / Settings.cozmo_turn_speed_degrees_per_second) * 1000
            TimingUtils.run_function_after_if_action_finished(turn_duration, turn_action,
                                                              self.drive_controller.continue_autonomous_behaviour)

        elif sign_count == 2:
            # Handling for two spotted signs
            self.do_packet_station_program()

    def reinitialize_for_lanetracking(self):
        self.drive_controller.stop_autonomous_behaviour()
        self.robot.drive_straight(distance_mm(-30), Speed(20), True, False, 3).wait_for_completed()
        self.robot.turn_in_place(degrees(180)).wait_for_completed()
        self.robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE + cozmo.util.degrees(4), in_parallel=True)
        self.robot.set_lift_height(1.0, in_parallel=True)
        self.robot.wait_for_all_actions_completed()
        self.trigger_sign_detection_cooldown()

    def do_packet_station_program(self):
        if not RobotStatusController.is_in_packetstation:
            print("Enter packetstation")
            RobotStatusController.is_in_packetstation = True
            Settings.cozmo_drive_speed = 20
            self.drive_controller.stop_autonomous_behaviour()
            PacketStation.packet_station_behavior(self.robot)
            self.drive_controller.continue_autonomous_behaviour()

        else:
            RobotStatusController.is_in_packetstation = False
            Settings.cozmo_drive_speed = 50
            print("Leaving packetstation")

    def search_for_faces_until_matching(self, is_matching):
        while not is_matching:
            RobotStatusController.perceived_faces = []
            RobotStatusController.perceived_faces.append(CubeFacePairing.look_for_faces(self.robot))
            is_matching = self.check_if_matching()
        action_speak = self.robot.say_text("Hier ist dein Würfel " + RobotStatusController.perceived_faces[0].name,
                                           in_parallel=True, use_cozmo_voice=False)
        action_drop = self.robot.place_object_on_ground_here(RobotStatusController.perceived_cubes[0],
                                                             in_parallel=True)
        action_speak.wait_for_completed()
        action_drop.wait_for_completed()

    def check_if_matching(self):
        return CubeFacePairing.compare_cube_and_face(self.robot, RobotStatusController.perceived_faces[0].name,
                                                     Settings.owner_dict[RobotStatusController.perceived_faces[0].name],
                                                     RobotStatusController.perceived_cubes[0].object_id,
                                                     RobotStatusController.perceived_faces[0])
