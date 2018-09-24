class RobotStatusController:

    # Set to true if Cozmo is in the packetstation, false otherwise
    is_in_packetstation = False

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
