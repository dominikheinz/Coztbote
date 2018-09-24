from Settings.CozmoSettings import Settings


class RobotStatusController:

    # How fast cozmo should currently drive
    drive_speed = Settings.cozmo_drive_speed

    # Set to true if Cozmo is in the packet station, false otherwise
    is_in_packet_station = False

    # If true sign detection is enabled, false otherwise
    scan_for_signs = False

    # Autonomous driving behavior
    disable_autonomous_behavior = False

    # Crossing detection
    is_at_crossing = False

    # Sign detection
    enable_sign_recognition = True
    sign_count = 0

    # Cozmo is holding a cube
    is_holding_cube = False
    holding_cube_id = None

    # Cozmo has not found a house matching with cube
    cube_undeliverable = False
