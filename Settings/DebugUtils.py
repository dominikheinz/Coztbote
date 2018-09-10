import time


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
