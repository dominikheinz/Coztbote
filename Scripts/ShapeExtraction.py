import cv2
import numpy
import operator
import random

image = cv2.imread("../Screenshots/Cozmo_2018-09-13-13-59-38.png")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray = 255 - gray

mask = numpy.full(gray.shape, 255, dtype=numpy.uint8)

contours = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]

biggest_contour_area = max(contours, key = cv2.contourArea)
cv2.drawContours(mask, [biggest_contour_area], 0, 0, -1)

cv2.imshow("Img", image)
cv2.imshow("Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(contours)
