import cv2
import numpy as np
from PIL import Image
from Engines.LaneTracking.PixelRow import PixelRow
from Engines.LaneTracking.LaneAnalyzer import LaneAnalyzer
from Settings.DebugUtils import DebugUtils


def show_pixel_line(title, line):
    lines = []

    for i in range(0, 30):
        lines.append(line)

    np_lines = np.array(lines)

    cv2.imshow(title, np_lines)


# pil_img = Image.open('./../../Screenshots/Screenshot-2018-09-11-09-30-24.jpg')
# pil_img = Image.open('./../../Screenshots/Screenshot-2018-09-11-09-30-38.jpg')
# pil_img = Image.open('./../../Screenshots/Screenshot-2018-09-11-09-30-39.jpg')
# pil_img = Image.open('./../../Screenshots/Screenshot-2018-09-11-09-30-41.jpg')
# pil_img = Image.open('./../../Screenshots/Screenshot-2018-09-11-09-30-44.jpg')
# pil_img = Image.open('./../../Screenshots/Screenshot-2018-09-11-10-23-32.png')
pil_img = Image.open('./../../Screenshots/index.jpg')
# pil_img.show()

# start calc
timer = DebugUtils.start_timer()

img = np.array(pil_img)

canny = cv2.Canny(img, 100, 200)

# crop image
canny = canny[:, 40:280]

rows_to_test = PixelRow.get_pixel_rows(canny)


analyzer = LaneAnalyzer()

# print(rows_to_test[0].left_edge_offset)
correction_value = analyzer.calculate_lane_correction(rows_to_test)

# end calc
timer.stop_timer()

cv2.imshow('Original', img)
cv2.imshow('Canny', canny)

print(correction_value)

cv2.waitKey(0)
cv2.destroyAllWindows()


