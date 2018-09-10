from enum import Enum


class GridField(Enum):
    upper_left = 0
    upper_middle = 1
    upper_right = 2

    middle_left = 3
    middle_middle = 4
    middle_right = 5

    bottom_left = 6
    bottom_middle = 7
    bottom_right = 8
