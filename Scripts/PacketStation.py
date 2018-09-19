import cozmo
from pynput import keyboard
from cozmo.util import degrees, distance_mm, speed_mmps, Angle
from Engines.RobotController import DriveController, RobotStatusController
from Engines.LaneTracking import LaneTrackingEngine
from Engines.LaneTracking import LaneAnalyzer
from Engines.SignHandler import SignHandler
from Utils.InstanceManager import InstanceManager
from Utils.PreviewUtils import PreviewUtils

from Engines.ImageRecognition.CubeFacePairing import CubeFacePairing

def handle_hotkeys(keycode):
    """
    Handle the keyboard key pressed event
    :param keycode: keycode of the pressed key
    :type keycode: pynput.keyboard.KeyCode
    """
    if keycode == keyboard.KeyCode(char='s') or keycode == keyboard.KeyCode(char='S'):
        preview_obj = InstanceManager.get_instance("PreviewUtils")
        preview_obj.save_cam_screenshot()

def packet_station(robot: cozmo.robot.Robot):
    CubeFacePairing.initialize(robot)
    perceived_cubes = []
    try:
        cube = CubeFacePairing.search_for_cube(robot, 10)
        print("Cube found")
        perceived_cubes.append(cube)
        print("Cube observed: " + cube.descriptive_name)
        robot.pickup_object(perceived_cubes[0], False, False, 10).wait_for_completed()
        robot.turn_in_place(degrees(180),False,1).wait_for_completed()

    except IndexError:
        print("No cube found in array!")

    #robot.turn_in_place().wait_for_completed()

    """
    Main script for the lane following algorithm. Starts all necessary components.
    :param robot_obj: Reference to the robot
    :type robot_obj: cozmo.robot.Robot
    """
    # Create necessary instances and add them to instance manager
    InstanceManager.add_instance("Robot", robot)

    lane_analyzer_obj = LaneAnalyzer.LaneAnalyzer()
    InstanceManager.add_instance("LaneAnalyzer", lane_analyzer_obj)

    preview_obj = PreviewUtils()
    InstanceManager.add_instance("PreviewUtils", preview_obj)

    drive_obj = DriveController.DriveController()
    InstanceManager.add_instance("RobotController", drive_obj)

    sign_handler_obj = SignHandler.SignHandler()
    InstanceManager.add_instance("SignHandler", sign_handler_obj)

    lane_tracking_obj = LaneTrackingEngine.LaneTrackingEngine()
    InstanceManager.add_instance("LaneTrackingEngine", lane_tracking_obj)

    # Setup robot with presets
    robot.enable_stop_on_cliff(False)
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled = False
    robot.set_head_light(False)
    robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE + cozmo.util.degrees(4), in_parallel=True)
    robot.set_lift_height(1.0, in_parallel=True)

    # Setup camera event handler
    robot.add_event_handler(cozmo.world.EvtNewCameraImage, lane_tracking_obj.process_frame)

    # Start driving engine if Robot state is in LaneTracing mode
    if RobotStatusController.RobotStatusController.current_state is \
            RobotStatusController.RobotStatusController.current_state.LANE_TRACING:
        drive_obj.go()

    # Setup hotkey listener
    with keyboard.Listener(on_press=handle_hotkeys) as listener:
        listener.join()

cozmo.run_program(packet_station)