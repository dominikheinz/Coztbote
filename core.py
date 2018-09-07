import cozmo
import time
from Engines.LaneTracking import LaneTrackingEngine


def start_cozmo_script(robot: cozmo.robot.Robot):
    # Setup Lanetracking Engine
    engine = LaneTrackingEngine.LaneTrackingEngine(robot)

    # Setup event handlers
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled = False

    time.sleep(1)

    robot.add_event_handler(cozmo.world.EvtNewCameraImage, engine.process_still_image)

    while True:
        pass


cozmo.run_program(start_cozmo_script)
