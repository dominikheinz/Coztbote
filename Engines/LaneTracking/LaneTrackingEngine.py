import cozmo
import PIL

class LaneTrackingEngine:

    def __init__(self):
        print("Processing still image")


    def ProcessStillImage(self, stillImage):
       image = cozmo.world.CameraImage(stillImage)
       rawImage = image.raw_image
       print(rawImage)