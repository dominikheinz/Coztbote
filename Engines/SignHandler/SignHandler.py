import datetime
import cozmo
from Settings.CozmoSettings import Settings
from Utils.InstanceManager import InstanceManager
from Engines.RobotController.RobotStatusController import RobotStatusController
from Engines.PacketStation import PacketStation
from Engines.PacketStation.CubeFacePairing import CubeFacePairing
from cozmo.util import degrees, distance_mm, Speed


class SignHandler:

    RobotStatusController = None
    robot = None

    def __init__(self):
        self.lane_analyzer = InstanceManager.get_instance("CorrectionCalculator")
        """
        Creating an instance of robot and getting the cooldown_time_ms from Settings.py
        """
        self.robot = InstanceManager.get_instance("Robot")
        self.cooldown_time = Settings.cooldown_time_ms

    def check_for_cooldown(self, time_sign_seen, disable_cooldown):
        """
        Checks last timestamp if time delta is exceeded, to block or 
        unblock sign_recognition_cooldown boolean
        :param time_sign_seen: time when sign is seen
        :param disable_cooldown: bool to disable cooldown functionality
        """

        if not disable_cooldown:
            # Checks if time interval is big enough to unlock the sign_recognition_cooldown
            if time_sign_seen < datetime.datetime.now() - datetime.timedelta(
                    milliseconds=self.cooldown_time) and RobotStatusController.sign_recognition_cooldown:
                RobotStatusController.sign_recognition_cooldown = False
                print("SignDetection: Cooldown is over")

            # Sets the cooldown for sign recognition if signs were seen, to prevent action looping
            if RobotStatusController.sign_count != 0 and RobotStatusController.sign_recognition_cooldown is False:
                RobotStatusController.sign_recognition_cooldown = True
                RobotStatusController.sign_count = 0    # Setting sign count to zero to prevent action looping
                print("SignDetection: Cooldown started")

    def react_to_signs(self, sign_count):
        """
        Tells Cozmo what to do for every sign(amount of signs)
        :param sign_count: amount of spotted signs
        """
        print(sign_count)
        if (sign_count % 2) is 1:
            # Handling for wrong identified signs, cause there als only even amount of signs
            print("Odd_Sign_Count_Error")

        elif sign_count is 4:
            # Handling for two spotted signs
            RobotStatusController.disable_autonomous_behavior = True
            self.robot.stop_all_motors()
            self.robot.set_lift_height(0.4).wait_for_completed()
            RobotStatusController.perceived_faces.append(CubeFacePairing.look_for_faces(self.robot))
            is_matching = self.check_if_matching()
            self.search_for_faces_until_matching(is_matching)

            self.reinitialize_for_lanetracking()

            self.robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE + cozmo.util.degrees(4), in_parallel=False)
            RobotStatusController.disable_autonomous_behavior = False

        elif sign_count is 6:
            # Handling for four spotted signs
            RobotStatusController.disable_autonomous_behavior = True
            self.robot.stop_all_motors()
            self.robot.turn_in_place(degrees(180)).wait_for_completed()
            RobotStatusController.action_start = datetime.datetime.now()
            RobotStatusController.action_cooldown_ms = Settings.wait_time_sign2

        elif sign_count is 2:
            self.do_packet_station_program()

    def reinitialize_for_lanetracking(self):
        RobotStatusController.disable_autonomous_behavior = True
        self.robot.stop_all_motors()
        self.robot.drive_straight(distance_mm(-30), Speed(20), True, False, 3).wait_for_completed()
        self.robot.turn_in_place(degrees(180)).wait_for_completed()
        self.robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE + cozmo.util.degrees(4), in_parallel=True)
        self.robot.set_lift_height(1.0, in_parallel=True)
        self.robot.wait_for_all_actions_completed()
        RobotStatusController.action_start = datetime.datetime.now()
        RobotStatusController.action_cooldown_ms = Settings.wait_time_sign2

    def do_packet_station_program(self):
        if not RobotStatusController.is_in_packetstation:
            print("Enter packetstation")
            RobotStatusController.is_in_packetstation = True
            Settings.cozmo_drive_speed = 20
            RobotStatusController.disable_autonomous_behavior = True
            self.robot.stop_all_motors()
            PacketStation.packet_station_behavior(self.robot)
            RobotStatusController.disable_autonomous_behavior = False

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

    @staticmethod
    def check_driving_cooldown():
        """
        Checks remaining cooldown time, to allow driving
        :return:
        """
        if RobotStatusController.action_start < datetime.datetime.now() - datetime.timedelta(
                milliseconds=RobotStatusController.action_cooldown_ms):
            RobotStatusController.disable_autonomous_behavior = False
