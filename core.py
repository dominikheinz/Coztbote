import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
from Engines.LaneTracking import LaneTrackingEngine


def cozmo_program(robot: cozmo.robot.Robot):
    # Process still image
    engine = LaneTrackingEngine.LaneTrackingEngine

    # Grab still image from cozmo
    robot.add_event_handler(cozmo.world.EvtNewCameraImage, engine.ProcessStillImage())

    robot.camera.image_stream_enabled = True

    while True:
        pass

cozmo.run_program(cozmo_program)