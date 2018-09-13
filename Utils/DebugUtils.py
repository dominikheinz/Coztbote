import time
import numpy


class DebugUtils:

    @staticmethod
    def start_timer():
        """
        Start a timer
        :return: A timer object
        """
        return DebugUtils.Timer()

    @staticmethod
    def stop_timer(timer, function_name):
        """
        Stops the timer and prints the duration
        :param timer: The timer to stop
        :param function_name: The timed function name which will be included in the console print
        """
        timer.stop_timer(function_name)

    class Timer:
        start_time = None

        def __init__(self):
            self.start_time = time.time()

        def stop_timer(self, function_name=""):
            """
            Stops the timer and prints the duration
            :param function_name: The timed function name which will be included in the console print
            """
            elapsed_time = time.time() - self.start_time
            print('{:s} function took {:.3f} ms'.format(function_name, elapsed_time * 1000.0))

    @staticmethod
    def unique_count(array):
        """
        Counts the unique array elements
        :param array: Array to count
        :return: Array with pairs of [ElementValue, ElementCount]
        """
        unique, inverse = numpy.unique(array, return_inverse=True)
        count = numpy.zeros(len(unique), numpy.int)
        numpy.add.at(count, inverse, 1)
        return numpy.vstack((unique, count)).T
