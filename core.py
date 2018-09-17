import cozmo
import numpy
from Scripts import LaneFollow


arr1 = [1,2,3]
arr2 = [4,5,6]
arr3 = [7,8,9]

sumarr = numpy.add(numpy.add(arr1, arr2), arr3)

cozmo.run_program(LaneFollow.run)
