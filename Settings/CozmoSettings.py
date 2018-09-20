class Settings:

    # Environment settings
    owner_dict = {"Eric": 0, "Fabian hehe": 1, "Fabian": 1, "Gero": 2, '': -1}  # -1 as error code for unknown access
    image_binarization_threshold = 30
    cooldown_time_ms = 5000
    disable_sign_detection = False
    disable_cooldown = False
    wait_time_sign1 = 4000  # wait time for stop sign
    wait_time_sign2 = 0     # wait time for turn around sign

    # Driving settings
    cozmo_enable_drive = True
    cozmo_drive_speed = 50
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
    crossing_horizontal_crop = 10
    crossing_vertical_crop = 60
    lane_pattern_min_width_threshold = 6

    # Measurement settings for contures
    min_pixel_sign = 150
    max_pixel_sign = 2000
    pixel_offset = 15
