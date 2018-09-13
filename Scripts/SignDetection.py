import cozmo
import time
import datetime
import cv2
from Engines.DriveController import DriveController
from Engines.LaneTracking import LaneTrackingEngine
from Engines.LaneTracking import LaneAnalyzer
from Utils import SignTrackingEngine
from Utils.InstanceManager import InstanceManager
from pynput import keyboard
from Utils.PreviewUtils import PreviewUtils


def run(robot_obj: cozmo.robot.Robot):
    # Add instances to instance manager
    InstanceManager.add_instance("Robot", robot_obj)

    lane_analyzer_obj = LaneAnalyzer.LaneAnalyzer()
    InstanceManager.add_instance("LaneAnalyzer", lane_analyzer_obj)

    preview_obj = PreviewUtils()
    InstanceManager.add_instance("PreviewUtils", preview_obj)

    drive_obj = DriveController.DriveController()
    InstanceManager.add_instance("DriveController", drive_obj)

    signtracking_obj = SignTrackingEngine.SignTrackingEngine()
    InstanceManager.add_instance("SignTrackingEngine", signtracking_obj)

    # Add instances to instance manager
    # Setup presets
    robot_obj.enable_stop_on_cliff(False)
    robot_obj.camera.image_stream_enabled = True
    robot_obj.camera.color_image_enabled = False
    robot_obj.set_head_light(False)
    robot_obj.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE + cozmo.util.degrees(4), in_parallel=True)
    robot_obj.set_lift_height(1.0, in_parallel=True)

    # Setup event handler
    robot_obj.add_event_handler(cozmo.world.EvtNewCameraImage, lanetracking_obj.process_still_image)

    # Start driving engine
    drive_obj.go()

    # Setup hotkey listener
    with keyboard.Listener(on_press=handle_hotkeys) as listener:
        listener.join()
