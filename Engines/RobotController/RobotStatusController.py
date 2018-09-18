class RobotStatusController:
    scan_for_signs = False

    is_at_crossing = False
    crossing_status = 0
    crossing_status_change_timestamp = None
    crossing_turn_degrees = 0
