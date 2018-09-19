import datetime

waiting_functions = []
finished_function_in_iteration = []


def run_function_after(delay_milliseconds, func, *args):
    """
    Runs a function after a specified amount of time
    :param delay_milliseconds: Delay, after which the function will be called. Exact execution time depends on how often
                               run_all_elapsed() is called.
    :param func: Function to call
    :param args: Parameters to pass to the function
    """
    waiting_functions.append(DelayedFunctionCall(delay_milliseconds, func, args))


def run_all_elapsed():
    """
    Run all functions whose delay has elapsed. Needs to be called in a loop.
    """
    for call in waiting_functions:
        is_done = call.run_if_elapsed()
        if is_done:
            # Save, so we can remove it later
            finished_function_in_iteration.append(call)

    for finished_function in finished_function_in_iteration:
        # Remove all finished functions from the waiting list
        waiting_functions.remove(finished_function)

    finished_function_in_iteration.clear()


class DelayedFunctionCall:
    run_at_time = None
    func = None
    args = None

    def __init__(self, delay_milliseconds, func, args):
        self.run_at_time = datetime.datetime.now() + datetime.timedelta(milliseconds=delay_milliseconds)
        self.func = func
        self.args = args

    def run_if_elapsed(self):
        """
        Run the saved function, if the specified execution time is right now or in the past
        """
        if self.run_at_time <= datetime.datetime.now():
            self.func(*self.args)
            return True
        return False
