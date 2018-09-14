from Settings.CozmoSettings import Settings
from Engines.LaneTracking.PixelRow import PixelRow


class LaneSegmentIdentifier:

    def __init__(self):
        pass

    def analyze_lane_segment(self, image):
        # Crop out relevant area
        image = self.crop_image(image)

        # Obtain pixel rows from shape
        rows = self.create_pixel_rows(image)

    def create_pixel_rows(img, step=40):
        """
        Extracts pixel rows from the image
        :param img: Source images
        :type img: Binary numpy array
        :param step: Pixel distance between each row
        :return: An array of PixelRow objects
        """
        h, w = img.shape
        pixel_rows = []

        for i in range(h, Settings.lane_segment_bottom_viewport_offset, step):
            pixel_rows.append(PixelRow(img[i]))
        return pixel_rows

    def crop_image(self, image):
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
