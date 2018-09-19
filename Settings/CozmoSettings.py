class Settings:

    # Environment settings
    image_binarization_threshold = 30
    cooldown_time_ms = 5000
    disable_sign_detection = True
    disable_cooldown = False
    wait_time_sign1 = 4000  # wait time for stop sign
    wait_time_sign2 = 0     # wait time for turn around sign

    # Driving settings
    cozmo_enable_drive = True
    cozmo_drive_speed = 70
    cozmo_turn_speed_slow_wheel = 0
    cozmo_turn_speed_fast_wheel = cozmo_drive_speed * 0.7

    # Live preview settings
    cozmo_show_cam_live_feed = True
    cozmo_img_processing_ms_limit = 40
    cozmo_preview_resolution = (1080, 720)
    cozmo_preview_screenshot_include_points = False
    show_contures_in_extra_window = True
    cozmo_lane_surrounding_width_px = 80

    # Lane segment identifier settings
    lane_segment_horizontal_viewport_offset = 10
    lane_segment_bottom_viewport_offset = 10
    lane_pattern_min_width_threshold = 6

    # Measurement settings for contures
    min_pixel_sign = 150
    max_pixel_sign = 1400
    pixel_offset = 15
