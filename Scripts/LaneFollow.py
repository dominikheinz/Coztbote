import cozmo
from pynput import keyboard
from Engines.RobotController import DriveController, RobotStatusController
from Engines import CoreEngine
from Engines.LaneTracking import CorrectionCalculator
from Engines.SignHandler import SignHandler
from Engines.RobotController import Navigator
from Utils.InstanceManager import InstanceManager
from Utils.PreviewUtils import PreviewUtils
from Utils import TimingUtils
from Scripts import LaneFollow
import sched, time

last_frame = None


def save_last_frame(e, image):
    LaneFollow.last_frame = image


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
    # Create necessary instances and add them to instance manager
    InstanceManager.add_instance("Robot", robot_obj)

    corr_calculator_obj = CorrectionCalculator.CorrectionCalculator()
    InstanceManager.add_instance("CorrectionCalculator", corr_calculator_obj)

    preview_obj = PreviewUtils()
    InstanceManager.add_instance("PreviewUtils", preview_obj)

    drive_obj = DriveController.DriveController()
    InstanceManager.add_instance("DriveController", drive_obj)

    navigator_obj = Navigator.Navigator()
    InstanceManager.add_instance("Navigator", navigator_obj)

    sign_handler_obj = SignHandler.SignHandler()
    InstanceManager.add_instance("SignHandler", sign_handler_obj)

    lane_tracking_obj = CoreEngine.CoreEngine()
    InstanceManager.add_instance("LaneTrackingEngine", lane_tracking_obj)

    # Setup robot with presets
    robot_obj.enable_stop_on_cliff(False)
    robot_obj.camera.image_stream_enabled = True
    robot_obj.camera.color_image_enabled = False
    robot_obj.set_head_light(False)
    robot_obj.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE + cozmo.util.degrees(4), in_parallel=True)
    robot_obj.set_lift_height(1.0, in_parallel=True)
    robot_obj.wait_for_all_actions_completed()

    # Setup camera event handler
    robot_obj.add_event_handler(cozmo.camera.EvtNewRawCameraImage, save_last_frame)

    # Start driving engine
    drive_obj.start()

    s = sched.scheduler(time.time, time.sleep)

    def run_analysis(sc):
        if LaneFollow.last_frame is not None:
            TimingUtils.run_all_elapsed()
            lane_tracking_obj.process_frame(image=LaneFollow.last_frame)
        s.enter(0.05, 1, run_analysis, (sc,))

    s.enter(0.05, 1, run_analysis, (s,))
    s.run()

    # Setup hotkey listener
    with keyboard.Listener(on_press=handle_hotkeys) as listener:
        listener.join()
