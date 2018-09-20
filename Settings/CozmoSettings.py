class Settings:

    # Image Preprocessor
    processing_frequency_ms = 40
    preprocessor_binarization_threshold = 30

    # Behavior
    disable_sign_detection = False
    disable_driving = False

    # Sign detection
    sign_detection_cooldown_time = 6000
    wait_time_sign1 = 4000  # wait time for stop sign
    wait_time_sign2 = 0     # wait time for turn around sign

    # Driving settings
    cozmo_drive_speed = 50
    cozmo_turn_speed_slow_wheel = 0
    cozmo_turn_speed_fast_wheel = cozmo_drive_speed * 0.7
    cozmo_turn_speed_degrees_per_second = 180

    # Live preview settings
    show_live_preview = True
    live_preview_resolution = (1080, 720)
    live_preview_screenshot_include_points = False
    live_preview_show_signs = True

    # Crossing settings
    crossing_horizontal_crop = 10
    crossing_vertical_crop = 60
    lane_pattern_min_width_threshold = 6
    crossing_approach_distance = 160

    # Sign detection settings
    sign_min_pixel_count = 150
    sign_max_pixel_count = 1800
    trigger_line_position = 185
