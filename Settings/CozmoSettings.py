class Settings:
    image_binarization_threshold = 50  # Maximum grey value to be mapped to 0, all above will be mapped to 1

    cozmo_enable_drive = False
    cozmo_drive_speed = 60
    cozmo_turn_speed_slow_wheel = 0  # Speed of the slower wheel while turning
    cozmo_turn_speed_fast_wheel = cozmo_drive_speed * 0.7  # Speed of the faster wheel wile turning
    cozmo_show_cam_live_feed = True
