import datetime
import cozmo
from cozmo.objects import LightCube3Id


class RobotStatusController:
    is_in_packetstation = False

    scan_for_signs = False

    is_at_crossing = False
    crossing_status = 0
    crossing_status_change_timestamp = None
    crossing_turn_degrees = 0

    disable_autonomous_behavior = False

    cooldown_start = None
    sign_count = 0
    sign_recognition_cooldown = False
    action_cooldown_ms = 0
    action_start = datetime.datetime.now()

    perceived_cubes = []
    perceived_faces = []
    face_recognized_but_not_matching = False
