import datetime

waiting_functions = []
finished_function_in_iteration = []


def run_function_after(delay_milliseconds, func, *args):
    waiting_functions.append(DelayedFunctionCall(delay_milliseconds, func, args))


def run_all_elapsed():
    for call in waiting_functions:
        is_done = call.run_if_elapsed()
        if is_done:
            finished_function_in_iteration .append(call)

    for finished_function in finished_function_in_iteration:
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
        if self.run_at_time <= datetime.datetime.now():
            self.func(*self.args)
            return True
        return False


