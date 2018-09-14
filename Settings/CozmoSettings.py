class Settings:

    # Environment settings
    image_binarization_threshold = 30

    # Driving settings
    cozmo_enable_drive = False  # WARNING TURNED OFF
    cozmo_drive_speed = 70
    cozmo_turn_speed_slow_wheel = 0
    cozmo_turn_speed_fast_wheel = cozmo_drive_speed * 0.7

    # Live preview settings
    cozmo_show_cam_live_feed = True
    cozmo_img_processing_ms_limit = 40
    cozmo_preview_resolution = (1080, 720)   # before: 1080, 720
    cozmo_preview_screenshot_include_points = True
    show_contures_in_extra_window = True

    # Measurement settings for contures
    min_pixel_sign = 150
    max_pixel_sign = 1200