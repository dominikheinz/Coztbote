from Settings.CozmoSettings import Settings
from Engines.LaneTracking.PixelRow import PixelRow


class LaneSegmentIdentifier:

    @staticmethod
    def analyze_lane_segment(image):
        # Crop out relevant area
        image = LaneSegmentIdentifier.crop_image(image)

        # Obtain pixel rows from shape
        rows = LaneSegmentIdentifier.create_pixel_rows(image)

        # Determine lane type based on pixel rows
        return LaneSegmentIdentifier.pixel_rows_to_lane_type(rows)


    @staticmethod
    def pixel_rows_to_lane_type(rows):
        if not rows:
            raise Exception("rows can not be null")

        # Determine lane type
        if LaneSegmentIdentifier.is_t_crossing(rows):
            pass # Placeholder
        elif LaneSegmentIdentifier.is_left_t_crossing(rows):
            pass # Placeholder
        elif LaneSegmentIdentifier.is_right_t_crossing(rows):
            pass # Placeholder
        elif LaneSegmentIdentifier.is_crossing(rows):
            pass # Placeholder
        else:
            pass # Single Lane

    @staticmethod
    def filter_invalid_row_pattern(rows):
        pass

    @staticmethod
    def is_left_t_crossing(rows):
        pass

    @staticmethod
    def is_right_t_crossing(rows):
        pass

    @staticmethod
    def is_t_crossing(rows):
        pass

    @staticmethod
    def is_crossing(rows):
        pass

    @staticmethod
    def create_pixel_rows(img, step=40):
        """
        Extracts pixel rows from the image
        :param img: Source images
        :type img: Binary numpy array
        :param step: Pixel distance between each row
        :return: An array of PixelRow objects from top to bottom
        """
        h, w = img.shape
        pixel_rows = []

        for i in range(int(h / 3), h - Settings.lane_segment_bottom_viewport_offset, step):
            pixel_rows.append(PixelRow(img[i]))
        return pixel_rows

    @staticmethod
    def crop_image(image):
        """
        Crops out the images sides by the specified offset as well as crops it
        to the lower 2/3rd of the image
        :param image: The input image that should be cropped
        :type image: Numpy array
        :return: Cropped image
        :rtype: Numpy array
        """
        offset = Settings.lane_segment_horizontal_viewport_offset
        h, w = image.shape
        return image[h / 3:h, offset:w - offset]
