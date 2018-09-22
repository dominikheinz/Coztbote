import cozmo
import sched
import time

from pynput import keyboard

from cozmo.camera import CameraConfig

from Controller.DriveController import DriveController
from Controller.BehaviorController import BehaviorController

from Engines.CoreEngine import CoreEngine
from Engines.LaneAnalyzer.CorrectionCalculator import CorrectionCalculator
from Engines.SignHandler.SignHandler import SignHandler
from Engines.Navigation.TrackLoader import TrackLoader
from Engines.Navigation.Navigator import Navigator

from Utils.InstanceManager import InstanceManager
from Utils.PreviewUtils import PreviewUtils
from Utils import TimingUtils

last_frame = None


# noinspection PyUnusedLocal
def save_last_frame(e, image):
    global last_frame
    last_frame = image


def handle_hotkeys(keycode):
    """
    Handle the keyboard key pressed event
    :param keycode: keycode of the pressed key
    :type keycode: pynput.keyboard.KeyCode
    """
    if keycode == keyboard.KeyCode(char='s') or keycode == keyboard.KeyCode(char='S'):
        preview_obj = InstanceManager.get_instance("PreviewUtils")
        preview_obj.save_cam_screenshot()


def run(robot_obj: cozmo.robot.Robot):
    """
    Main script for the lane following algorithm. Starts all necessary components.
    :param robot_obj: Reference to the robot
    :type robot_obj: cozmo.robot.Robot
    """
    global last_frame

    # Create necessary instances and add them to instance manager
    InstanceManager.add_instance("Robot", robot_obj)

    corr_calculator_obj = CorrectionCalculator()
    InstanceManager.add_instance("CorrectionCalculator", corr_calculator_obj)

    preview_obj = PreviewUtils()
    InstanceManager.add_instance("PreviewUtils", preview_obj)

    drive_obj = DriveController()
    InstanceManager.add_instance("DriveController", drive_obj)

    behavior_obj = BehaviorController()
    InstanceManager.add_instance("BehaviorController", behavior_obj)

    trackloader_obj = TrackLoader()
    InstanceManager.add_instance("TrackLoader", trackloader_obj)

    navigator_obj = Navigator()
    InstanceManager.add_instance("Navigator", navigator_obj)

    sign_handler_obj = SignHandler()
    InstanceManager.add_instance("SignHandler", sign_handler_obj)

    core_engine_obj = CoreEngine()
    InstanceManager.add_instance("CoreEngine", core_engine_obj)

    # Setup robot with presets
    robot_obj.enable_stop_on_cliff(False)
    robot_obj.camera.image_stream_enabled = True
    robot_obj.camera.color_image_enabled = False
    robot_obj.set_head_light(False)
    robot_obj.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE + cozmo.util.degrees(4), in_parallel=True)
    robot_obj.set_lift_height(1.0, in_parallel=True)
    robot_obj.wait_for_all_actions_completed()

    # ToDo change position of set route
    Navigator.set_route(0, 2)

    # Setup camera event handler
    # noinspection PyTypeChecker
    robot_obj.add_event_handler(cozmo.camera.EvtNewRawCameraImage, save_last_frame)

    # Start driving engine
    drive_obj.start()

    s = sched.scheduler(time.time, time.sleep)

    def run_analysis(sc):
        if last_frame is not None:
            TimingUtils.run_all_elapsed()
            core_engine_obj.process_frame(image=last_frame)
        s.enter(0.05, 1, run_analysis, (sc,))

    s.enter(0.05, 1, run_analysis, (s,))
    s.run()

    # Setup hotkey listener
    with keyboard.Listener(on_press=handle_hotkeys) as listener:
        listener.join()
