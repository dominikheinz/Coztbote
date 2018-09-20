from enum import Enum


class RobotStatusController:

    class BehaviorState(Enum):
        PACKET_FINDING = 1
        LANE_TRACKING = 2
        FACE_PAIRING = 3

    # Behavior states
    current_state = BehaviorState.PACKET_FINDING

    # Autonomous driving behavior
    disable_autonomous_behavior = False

    # Crossing detection
    is_at_crossing = False

    # Sign detection
    enable_sign_recognition = True
    sign_count = 0
