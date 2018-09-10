import cozmo
import time
from Engines.DriveController import DriveController
from Engines.LaneTracking import LaneTrackingEngine


def start_cozmo_script(robot: cozmo.robot.Robot):
    # Setup Lanetracking Engine
    drive_controller = DriveController.DriveController(robot)
    engine = LaneTrackingEngine.LaneTrackingEngine(robot, drive_controller)

    # Setup event handlers
    robot.enable_stop_on_cliff(False)
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled = False
    robot.set_head_light(False)
    robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE + cozmo.util.degrees(4), in_parallel=True)
    robot.set_lift_height(1.0, in_parallel=True)

    time.sleep(1)

    robot.add_event_handler(cozmo.world.EvtNewCameraImage, engine.process_still_image)

    drive_controller.go()

    print("Battery Voltage:", robot.battery_voltage)

    while True:
        pass


cozmo.run_program(start_cozmo_script)
