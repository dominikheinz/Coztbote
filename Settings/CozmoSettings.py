class Settings:

    # Environment settings
    image_binarization_threshold = 30
    disable_sign_detection = False
    disable_cooldown = False
    sign_detection_cooldown_time = 6000
    wait_time_sign1 = 4000  # wait time for stop sign
    wait_time_sign2 = 0     # wait time for turn around sign

    # Driving settings
    cozmo_enable_drive = True
    cozmo_drive_speed = 50
    cozmo_turn_speed_slow_wheel = 0
    cozmo_turn_speed_fast_wheel = cozmo_drive_speed * 0.7
    cozmo_turn_speed_degrees_per_second = 180

    # Live preview settings
    cozmo_show_cam_live_feed = True
    cozmo_img_processing_ms_limit = 40
    cozmo_preview_resolution = (1080, 720)
    cozmo_preview_screenshot_include_points = False
    show_contures_in_extra_window = True
    cozmo_lane_surrounding_width_px = 80

    cozmo_crossing_approach_distance = 160

    # Lane segment identifier settings
    crossing_horizontal_crop = 10
    crossing_vertical_crop = 60
    lane_pattern_min_width_threshold = 6

    # Measurement settings for contures
    min_pixel_sign = 150
    max_pixel_sign = 1400
    pixel_offset = 15
