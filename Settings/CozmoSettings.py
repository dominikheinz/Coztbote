class Settings:
    """ Environment settings """
    # -1 as error code for unknown access
    owner_dict = {"Schäffer": 0, "Brechtel": 1, "Faltin": 1, "Reinhardt": 2, "Heinz": 3, "Knoblauch": 3, '': -1}
    image_binarization_threshold = 25

    """ Image Preprocessor """
    processing_frequency_ms = 40
    preprocessor_binarization_threshold = 30

    """ Behavior """
    disable_sign_detection = False
    disable_driving = False

    """ Sign detection """
    sign_detection_cooldown_ms = 5000
    wait_time_sign1 = 4000  # wait time for stop sign
    wait_time_sign2 = 0  # wait time for turn around sign

    """ Driving settings """
    cozmo_drive_speed = 50
    cozmo_packet_station_drive_speed = 35
    cozmo_turn_speed_slow_wheel = 0
    cozmo_turn_speed_fast_wheel = cozmo_drive_speed * 0.8
    cozmo_turn_speed_degrees_per_second = 180

    """ Live preview settings """
    show_live_preview = True
    live_preview_resolution = (1080, 720)
    live_preview_screenshot_include_points = False
    live_preview_show_signs = False
    live_preview_show_crossing_detection_region = False

    """ Crossing settings """
    crossing_top_crop = 90
    crossing_bottom_crop = 30
    crossing_left_crop = 10
    crossing_right_crop = 10
    # Minimum distance the correction point has to have from the frame edge to be a valid crossing
    crossing_correction_min_dist_to_edge = 60

    lane_pattern_min_width_threshold = 6
    crossing_approach_distance = 100

    """ Sign detection settings """
    sign_min_pixel_count = 120
    sign_max_pixel_count = 2000
    trigger_line_position = 185

    """ All TTS """
    tts_packet_delivered = "Paket zugestellt, schönen Tag noch, Herr "
    tts_wrong_house_personal = "Verzeihung, bin hier wohl falsch, Herr "
    tts_wrong_house = "Verzeihung, bin hier wohl falsch."
