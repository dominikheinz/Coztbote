import cv2
import numpy


def unique_count(a):
    unique, inverse = numpy.unique(a, return_inverse=True)
    count = numpy.zeros(len(unique), numpy.int)
    numpy.add.at(count, inverse, 1)
    return numpy.vstack((unique, count)).T


image = cv2.imread("Screenshots/Screenshot-2018-09-11-10-13-52.png", cv2.IMREAD_GRAYSCALE) - 255

print(unique_count(image))
print(image)

start_row_1 = int(image.shape[0] / 3)
row_height = int((image.shape[0] - start_row_1) / 3)
end_row_1 = start_row_1 + row_height
end_row_2 = end_row_1 + row_height
end_row_3 = image.shape[0]

x_row_1 = int(numpy.mean(numpy.nonzero(image[start_row_1:end_row_1])[1]))
x_row_2 = int(numpy.mean(numpy.nonzero(image[end_row_1:end_row_2])[1]))
x_row_3 = int(numpy.mean(numpy.nonzero(image[end_row_2:end_row_3])[1]))

#numpy.set_printoptions(threshold=numpy.nan)
print(x_row_1)
print(x_row_2)
print(x_row_3)

image = (image + 255)

print(unique_count(image))
print(image)

image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

cv2.circle(image, (x_row_1, int((start_row_1 + end_row_1) / 2)), radius=3, color=(0, 0, 255), thickness=5)
cv2.circle(image, (x_row_2, int((end_row_1 + end_row_2) / 2)), radius=3, color=(0, 0, 255), thickness=5)
cv2.circle(image, (x_row_3, int((end_row_2 + end_row_3) / 2)), radius=3, color=(0, 0, 255), thickness=5)

cv2.imshow("img", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
