from cv2 import *
import numpy
import datetime
from Engines.LaneTracking.ImagePreprocessor import ImagePreprocessor


class LaneTrackingEngine:
    robot = None
    last_timestamp = None

    def __init__(self, robot):
        self.robot = robot
        self.last_timestamp = datetime.datetime.now()
        pass

    def process_still_image(self, e, image):
        if self.last_timestamp < datetime.datetime.now() - datetime.timedelta(milliseconds=300):
            processor = ImagePreprocessor()
            img_raw = image.raw_image
            img_bw = processor.rgb_to_bw(img_raw)
            cv2.imshow("Cam1", numpy.multiply(img_bw, 255 * 255))
            cv2.waitKey(1)

            self.last_timestamp = datetime.datetime.now()

            print(self.robot.camera.exposure_ms)
