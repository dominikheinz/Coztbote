import numpy
from Settings.CozmoSettings import Settings
from Utils.InstanceManager import InstanceManager
from Utils.ImagePreprocessor import ImagePreprocessor
from Engines.LaneAnalyzer.CrossingType import CrossingType


class CrossingTypeIdentifier:
    last_crossing_type = None
    last_confirmed_crossing_type = None
    correction_calculator_obj = None

    @staticmethod
    def analyze_frame(image):
        """
        Analyzes a frame to check it it contains a crossing. A crossing type needs to stay unchanged for 2 frames
        for it to be confirmed as valid and returned.
        :param image: The image as captured by Cozmos camera
        :return: The last confirmed crossing type
        """
        correction_calculator_obj = InstanceManager.get_instance("CorrectionCalculator")

        # If lane correction is too much the crossing may be invalid and should be discarded
        correction_points = correction_calculator_obj.last_points
        if correction_points is None or correction_points[0] is None or \
                correction_points[0][0] < Settings.crossing_correction_min_dist_to_edge or \
                correction_points[0][0] > image.shape[1] - Settings.crossing_correction_min_dist_to_edge:
            CrossingTypeIdentifier.last_confirmed_crossing_type = None
            return CrossingTypeIdentifier.last_confirmed_crossing_type

        # Crop out relevant area
        image = ImagePreprocessor.crop_image(image, Settings.crossing_top_crop, Settings.crossing_right_crop,
                                             Settings.crossing_bottom_crop, Settings.crossing_left_crop)

        # Obtain pixel rows from shape
        row_patterns = CrossingTypeIdentifier.create_row_patterns(image)

        # Filter out invalid patterns
        row_patterns = CrossingTypeIdentifier.filter_invalid_row_pattern(row_patterns)

        # Set last crossing type for preview window
        crossing_type = CrossingTypeIdentifier.row_patterns_to_crossing_type(row_patterns)

        # Confirm crossing type if at least on two frames
        if crossing_type == CrossingTypeIdentifier.last_crossing_type:
            CrossingTypeIdentifier.last_confirmed_crossing_type = crossing_type
        else:
            CrossingTypeIdentifier.last_confirmed_crossing_type = None

        CrossingTypeIdentifier.last_crossing_type = crossing_type

        return CrossingTypeIdentifier.last_confirmed_crossing_type

    @staticmethod
    def row_patterns_to_crossing_type(rows):
        """
        Convert a row pattern array to a crossing type
        :param rows:
        :return:
        """
        # Determine lane type
        if CrossingTypeIdentifier.is_t_crossing(rows):
            return CrossingType.T_Crossing
        elif CrossingTypeIdentifier.is_left_t_crossing(rows):
            return CrossingType.Left_T_Crossing
        elif CrossingTypeIdentifier.is_right_t_crossing(rows):
            return CrossingType.Right_T_Crossing
        elif CrossingTypeIdentifier.is_crossing(rows):
            return CrossingType.Crossing
        else:
            return None  # Single Lane

    @staticmethod
    def filter_invalid_row_pattern(row_patterns):
        """
        Filters out invalid row patterns based on how often they occur.
        :param row_patterns: Raw row patterns
        :return: Filtered row patterns
        """
        pattern_count = []

        for i, pattern in enumerate(row_patterns):
            pattern = list(pattern)
            if i == 0:
                pattern_count.append([pattern, 1])
            elif pattern_count[-1][0] == pattern:
                pattern_count[-1][1] += 1
            else:
                pattern_count.append([pattern, 1])

        # Group patterns into the 3 most common sub groups
        def func(arg):
            return arg[1]

        while len(pattern_count) > 3:
            smallest = min(pattern_count, key=func)
            pattern_count.remove(smallest)

            # combine patterns if they are next to each other
            to_delete = []
            for i, pattern in enumerate(pattern_count):
                if i == 0:
                    continue

                elif pattern_count[i][0] == pattern_count[i - 1][0]:
                    pattern_count[i][1] += pattern_count[i - 1][1]
                    to_delete.insert(0, i - 1)

            for i in to_delete:
                del pattern_count[i]

        pattern_count = numpy.array(pattern_count)

        return pattern_count[:, 0]

    @staticmethod
    def is_left_t_crossing(row_patterns):
        """
        Checks if pattern matches left T-crossing
        :param row_patterns: Filtered row patterns
        :return: True if pattern matched, false otherwise
        """

        # Ensure that we only have 3 rows
        if len(row_patterns) != 3:
            return False

        # Match row pattern
        if numpy.array_equal(row_patterns[0], [1, 0, 1]) and \
                numpy.array_equal(row_patterns[1], [0, 1]) and \
                numpy.array_equal(row_patterns[2], [1, 0, 1]):
            return True
        return False

    @staticmethod
    def is_right_t_crossing(row_patterns):
        """
        Checks if pattern matches right T-crossing
        :param row_patterns: Filtered row patterns
        :return: True if pattern matched, false otherwise
        """

        # Ensure that we only have 3 rows
        if len(row_patterns) != 3:
            return False

        # Match row pattern
        if numpy.array_equal(row_patterns[0], [1, 0, 1]) and \
                numpy.array_equal(row_patterns[1], [1, 0]) and \
                numpy.array_equal(row_patterns[2], [1, 0, 1]):
            return True
        return False

    @staticmethod
    def is_t_crossing(row_patterns):
        """
        Checks if pattern matches T-crossing
        :param row_patterns: Filtered row patterns
        :return: True if pattern matched, false otherwise
        """

        # Ensure that we only have 3 rows
        if len(row_patterns) != 3:
            return False

        # Match row pattern
        if numpy.array_equal(row_patterns[0], [1]) and \
                numpy.array_equal(row_patterns[1], [0]) and \
                numpy.array_equal(row_patterns[2], [1, 0, 1]):
            return True
        return False

    @staticmethod
    def is_crossing(row_patterns):
        """
        Checks if pattern matches crossing
        :param row_patterns: Filtered row patterns
        :return: True if pattern matched, false otherwise
        """

        # Ensure that we only have 3 rows
        if len(row_patterns) != 3:
            return False

        # Match row pattern
        if numpy.array_equal(row_patterns[0], [1, 0, 1]) and \
                numpy.array_equal(row_patterns[1], [0]) and \
                numpy.array_equal(row_patterns[2], [1, 0, 1]):
            return True
        return False

    @staticmethod
    def create_row_patterns(img, step=10):
        """
        Extracts pixel rows from the image
        :param img: Source images
        :type img: Binary numpy array
        :param step: Pixel distance between each row
        :return: An array of row patterns from top to bottom
        """
        h, w = img.shape
        row_patterns = []

        for i in range(0, h, step):
            rle_data = ImagePreprocessor.run_length_encoding(img[i])
            detailed_pattern = ImagePreprocessor.cleanup_row_noise(rle_data)
            row_patterns.append(detailed_pattern[:, 1])

        return row_patterns
