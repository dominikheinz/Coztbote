import time
import numpy


class DebugUtils:

    @staticmethod
    def start_timer():
        return DebugUtils.Timer()

    @staticmethod
    def stop_timer(timer, function_name):
        timer.stop_timer(function_name)

    class Timer:
        start_time = None

        def __init__(self):
            self.start_time = time.time()

        def stop_timer(self, function_name=""):
            elapsed_time = time.time() - self.start_time
            print('{:s} function took {:.3f} ms'.format(function_name, elapsed_time * 1000.0))

    def unique_count(array):
        unique, inverse = numpy.unique(array, return_inverse=True)
        count = numpy.zeros(len(unique), numpy.int)
        numpy.add.at(count, inverse, 1)
        return numpy.vstack((unique, count)).T
