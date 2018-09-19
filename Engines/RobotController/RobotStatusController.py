import datetime
from enum import Enum


class RobotStatusController:
    class BehaviorState(Enum):
        PACKET_FINDING = 1
        LANE_TRACING = 2
        FACE_PAIRING = 3

    scan_for_signs = True
    cooldown_start = None
    sign_count = 0
    sign_recognition_cooldown = False
    action_cooldown_ms = 0
    action_start = datetime.datetime.now()
    current_state = BehaviorState.PACKET_FINDING
