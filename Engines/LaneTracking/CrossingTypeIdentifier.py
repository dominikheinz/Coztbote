import numpy
from Settings.CozmoSettings import Settings
from Engines.LaneTracking.PixelRow import PixelRow
from Engines.LaneTracking.ImagePreprocessor import ImagePreprocessor
from Utils.DebugUtils import DebugUtils


class LaneSegmentIdentifier:

    @staticmethod
    def analyze_lane_segment(image):
        # Crop out relevant area
        image = LaneSegmentIdentifier.crop_image(image)

        # Obtain pixel rows from shape
        row_patterns = LaneSegmentIdentifier.create_row_patterns(image)

        row_patterns = LaneSegmentIdentifier.filter_invalid_row_pattern(row_patterns)
        # Determine lane type based on pixel rows
        return LaneSegmentIdentifier.row_patterns_to_lane_type(row_patterns)

    @staticmethod
    def row_patterns_to_lane_type(rows):
        if not rows:
            raise Exception("rows can not be null")

        # Determine lane type
        if LaneSegmentIdentifier.is_t_crossing(rows):
            pass  # Placeholder
        elif LaneSegmentIdentifier.is_left_t_crossing(rows):
            pass  # Placeholder
        elif LaneSegmentIdentifier.is_right_t_crossing(rows):
            pass  # Placeholder
        elif LaneSegmentIdentifier.is_crossing(rows):
            pass  # Placeholder
        else:
            pass  # Single Lane

    @staticmethod
    def filter_invalid_row_pattern(row_patterns):

        # [
        # [pattern A, how often does A occur consecutively],
        # [pattern B, how often does B occur consecutively]
        # ]
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
    def is_left_t_crossing(rows):
        # 1 0 1
        # 0 - 1
        # 1 0 1

        # Ensure that we only have 3 rows
        if len(rows) != 3:
            return False

        # Match row pattern
        if numpy.array_equal(rows[0], [1, 0, 1]) and \
                numpy.array_equal(rows[1], [0, 1]) and \
                numpy.array_equal(rows[2], [1, 0, 1]):
            return True
        return False

    @staticmethod
    def is_right_t_crossing(rows):
        # 1 0 1
        # 1 0 -
        # 1 0 1

        # Ensure that we only have 3 rows
        if len(rows) != 3:
            return False

        # Match row pattern
        if numpy.array_equal(rows[0], [1, 0, 1]) and \
                numpy.array_equal(rows[1], [1, 0]) and \
                numpy.array_equal(rows[2], [1, 0, 1]):
            return True
        return False

    @staticmethod
    def is_t_crossing(rows):
        # 1 - -
        # 0 - -
        # 1 0 1

        # Ensure that we only have 3 rows
        if len(rows) != 3:
            return False

        # Match row pattern
        if numpy.array_equal(rows[0], [1]) and \
                numpy.array_equal(rows[1], [0]) and \
                numpy.array_equal(rows[2], [1, 0, 1]):
            return True
        return False

    @staticmethod
    def is_crossing(rows):
        # 1 0 1
        # 0 - -
        # 1 0 1

        # Ensure that we only have 3 rows
        if len(rows) != 3:
            return False

        # Match row pattern
        if numpy.array_equal(rows[0], [1, 0, 1]) and \
                numpy.array_equal(rows[1], [0]) and \
                numpy.array_equal(rows[2], [1, 0, 1]):
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

    @staticmethod
    def crop_image(image):
        """
        Crops out the image by the offsets specified in settings
        :param image: The input image that should be cropped
        :type image: Numpy array
        :return: Cropped image
        :rtype: Numpy array
        """
        h_offset = Settings.lane_segment_horizontal_viewport_offset
        v_offset = Settings.lane_segment_vertical_viewport_offset
        h, w = image.shape
        return image[v_offset:h - v_offset, h_offset:w - h_offset]
