import datetime
class RobotStatusController:
    scan_for_signs = True
    cooldown_start = None
    sign_count = 0
    sign_recognition_cooldown = False
    action_cooldown_ms = datetime.datetime.now()
    action_start = None
