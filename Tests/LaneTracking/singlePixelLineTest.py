import cv2
import numpy as np


def print_pixel_line(line):
    lines = []

    for i in range(0, 30):
        lines.append(line)

    np_lines = np.array(lines)

    cv2.imshow('Pixel Line', np_lines)


# img = cv2.imread('./../../Screenshots/Screenshot-2018-09-11-09-30-24.jpg')
# img = cv2.imread('./../../Screenshots/Screenshot-2018-09-11-09-30-38.jpg')
# img = cv2.imread('./../../Screenshots/Screenshot-2018-09-11-09-30-39.jpg')
# img = cv2.imread('./../../Screenshots/Screenshot-2018-09-11-09-30-41.jpg')
# img = cv2.imread('./../../Screenshots/Screenshot-2018-09-11-09-30-44.jpg')
img = cv2.imread('./../../Screenshots/Screenshot-2018-09-11-10-23-32.png')

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_gray = img_gray[:, 40:280]

line_number = 200

img[line_number] = [0, 0, 255]

canny = cv2.Canny(img_gray, 100, 200)

cv2.imshow('Original', img)
cv2.imshow('Canny', canny)

print_pixel_line(canny[line_number])

cv2.waitKey(0)
cv2.destroyAllWindows()
