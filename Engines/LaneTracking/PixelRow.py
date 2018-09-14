from itertools import groupby
from Utils.DebugUtils import DebugUtils
from Settings.CozmoSettings import Settings
import numpy


class PixelRow:

    pattern = None
    b_w_count = None

    def __init__(self, raw_row):

        self.raw_row = raw_row

        self.raw_b_w_count = self.run_length_encoding(raw_row)

        # Julians Version
        self.clean_row()

        # Fabis Version
        self.eliminate_noise()

        print(self.b_w_count)

    def run_length_encoding(self, data):
        return numpy.array([[len(list(group)), name] for name, group in groupby(data)])

    def eliminate_noise(self):

        new_list = [[0, -1]]

        last_segment_was_invalid = False

        for i in range(self.raw_b_w_count.shape[0]):

            amount = self.raw_b_w_count[i, 0]

            if self.raw_b_w_count[i, 0] < Settings.lane_pattern_min_width_threshold:

                new_list[-1][0] += amount
                new_list[-1][1] = 1 - self.raw_b_w_count[i]

                last_segment_was_invalid = True

            elif last_segment_was_invalid:
                new_list[-1][0] += amount
                last_segment_was_invalid = False

            else:
                new_list.append([amount, self.raw_b_w_count[i, 0]])

        self.b_w_count = numpy.array(new_list)

    def clean_row(self):
        self.b_w_count = []

        last_segment_was_invalid = False

        for i, segment in self.raw_b_w_count:
            if segment[0] < Settings.lane_pattern_min_width_threshold:
                if self.raw_b_w_count.shape[0] == 0:
                    # Append element with inverted value
                    self.b_w_count.append([segment[0], 1 - segment[1]])
                else:
                    # Add count to last element
                    self.b_w_count[-1][0] += segment[0]
                last_segment_was_invalid = True
            else:
                if last_segment_was_invalid:
                    # Add count to last element
                    self.b_w_count[-1][0] += segment[0]
                else:
                    # Append new value
                    self.b_w_count.append([segment[0], 1 - segment[1]])

                last_segment_was_invalid = False

            self.b_w_count = numpy.array(self.b_w_count)
