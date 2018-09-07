import cozmo
import time
from cv2 import *
from Engines.LaneTracking import LaneTrackingEngine


def start_cozmo_script(robot: cozmo.robot.Robot):
    # Setup Lanetracking Engine
    engine = LaneTrackingEngine.LaneTrackingEngine

    # Setup event handlers
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled = True

    time.sleep(1)

    robot.add_event_handler(cozmo.world.EvtNewCameraImage, engine.process_still_image)

    # Sleep 1 second before exit
    time.sleep(1)


cozmo.run_program(start_cozmo_script)
