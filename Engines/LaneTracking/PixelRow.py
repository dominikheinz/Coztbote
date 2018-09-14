import numpy
from itertools import groupby
from Settings.CozmoSettings import Settings
from LaneTracking.ImagePreprocessor import ImagePreprocessor


class PixelRow:

    pattern = None
    b_w_count = None

    def __init__(self, raw_row):
        self.raw_b_w_count = ImagePreprocessor.run_length_encoding(raw_row)
        self.eliminate_noise()


    def eliminate_noise(self):
        """
        Remove pixel runs, which are too short to be valid
        """
        new_list = [[0, -1]]
        last_run_too_short = False

        for i in range(self.raw_b_w_count.shape[0]):

            run_length = self.raw_b_w_count[i, 0]
            run_color = self.raw_b_w_count[i, 1]

            run_too_small = lambda x: x < Settings.lane_pattern_min_width_threshold
            list_is_empty = lambda: new_list[0][1] == -1

            # Run is too small -> run is added to previous run
            if run_too_small(run_length):
                # Add run length to last valid run
                new_list[-1][0] += run_length
                last_run_too_short = True

            elif last_run_too_short:
                # If last valid run was same color add to it, otherwise create new run
                if new_list[-1][1] == run_color or list_is_empty():
                    new_list[-1][0] += run_length
                    # Set color, in case last run is still -1
                    new_list[-1][1] = run_color
                else:
                    new_list.append(self.raw_b_w_count[i])

                last_run_too_short = False

            # Run is okay, add run to new list as is
            else:
                if list_is_empty():
                    new_list[0] = self.raw_b_w_count[i]
                else:
                    new_list.append(self.raw_b_w_count[i])

        self.b_w_count = numpy.array(new_list)
