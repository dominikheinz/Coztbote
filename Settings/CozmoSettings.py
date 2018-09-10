class Settings:
    image_binarization_threshold = 50  # Maximum grey value to be mapped to 0, all above will be mapped to 1

    cozmo_dive_speed = 40
    cozmo_turn_speed_slow_wheel = cozmo_dive_speed * 0.05  # Speed of the slower wheel while turning
    cozmo_turn_speed_fast_wheel = cozmo_dive_speed * 0.7  # Speed of the faster wheel wile turning
