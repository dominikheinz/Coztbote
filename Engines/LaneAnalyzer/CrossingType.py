from enum import Enum


class CrossingType(Enum):
    Crossing = 0,
    T_Crossing = 1,
    Left_T_Crossing = 2,
    Right_T_Crossing = 3

    @staticmethod
    def get_crossing_as_string(crossing_type):
        """
        Converts a crossing type to a displayable string
        :param crossing_type: The crossing type enum
        :return: String of the name of the crossing type
        """
        if crossing_type == CrossingType.Left_T_Crossing:
            return "Left T-Crossing"
        elif crossing_type == CrossingType.Right_T_Crossing:
            return "Right T-Crossing"
        elif crossing_type == CrossingType.Crossing:
            return "Crossing"
        elif crossing_type == CrossingType.T_Crossing:
            return "T-Crossing"
