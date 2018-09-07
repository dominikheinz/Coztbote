from cv2 import *
from Engines.LaneTracking.ImagePreprocessor import ImagePreprocessor

class LaneTrackingEngine:

    def __init__(self):
        pass

    def process_still_image(self, image):
       processor = ImagePreprocessor()
       img_raw = image.raw_image
       img_bw = processor.rgb_to_bw(img_raw)
       img_bw.show()
       exit(0)