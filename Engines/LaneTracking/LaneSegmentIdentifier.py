import numpy
import cv2
from Settings.CozmoSettings import Settings


class LaneSegmentIdentifier:

    def __init__(self):
        pass

    def analyze_lane_segment(self, image):

        # Crop out relevant area
        image = self.crop_image(image)

        # Extract road shape
        road_shape = self.extract_road_shape(image)

        # Extract the pixel stripes
        pixel_pattern = self.extract_pixelpattern(image[ ?? ])

        if pixel_pattern == aaa:
            bla
        elif pixel_pattern == bbb:
            blabla

    def calculate_pixel_pattern(self, image):
        pixel_row1 =  self.create_pixel_row(image, 26)
        pixel_row2 = self.create_pixel_row(image, 92)
        pixel_row3 = self.create_pixel_row(image, 145)

    def create_pixel_row(self, image, y_pos):

        # Sum rows along y axis

        summed_row = numpy.add(numpy.add(top_row, middle_row), bottom_row)

        # If at most one pixel was white set it to black
        return numpy.array(summed_row < 2, dtype=numpy.uint8)

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
        return image[start_h / 3:h, offset:w - offset]
