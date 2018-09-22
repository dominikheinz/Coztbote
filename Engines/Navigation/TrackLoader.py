class TrackLoader:
    street_map = {
        (0, 1): ['R'],
        (0, 2): ['S'],
        (0, 3): ['L', 'R'],
        (0, 4): ['L', 'S', 'S', 'S'],
        (0, 5): ['L', 'S', 'L', 'S'],

        (1, 0): ['L'],
        (1, 2): ['R'],
        (1, 3): ['S', 'R'],
        (1, 4): ['S', 'S', 'S', 'S'],
        (1, 5): ['S', 'S', 'L', 'S'],

        (2, 0): ['S'],
        (2, 1): ['L'],
        (2, 3): ['R', 'R'],
        (2, 4): ['R', 'S', 'S', 'S'],
        (2, 5): ['R', 'S', 'L', 'S'],

        (3, 0): ['L', 'R'],
        (3, 1): ['L', 'S'],
        (3, 2): ['L', 'L'],
        (3, 4): ['R', 'S', 'S'],
        (3, 5): ['R', 'L', 'S'],

        (4, 0): ['S', 'S', 'S', 'R'],
        (4, 1): ['S', 'S', 'S', 'S'],
        (4, 2): ['S', 'S', 'S', 'L'],
        (4, 3): ['S', 'S', 'L'],
        (4, 5): ['R'],

        (5, 0): ['S', 'R', 'S', 'R'],
        (5, 1): ['S', 'R', 'S', 'S'],
        (5, 2): ['S', 'R', 'S', 'L'],
        (5, 3): ['S', 'R', 'L'],
        (5, 4): ['L'],
    }

    @staticmethod
    def load_track(start, end):
        """
        Finds the matching track for given start and endpoint
        :param start: The start point
        :param end: The end point
        :return: The track to navigate from start to end
        """

        # Find matching tracks for given start and end
        route = TrackLoader.street_map.get((start, end))

        # If route was not found throw an exception
        if route is None:
            raise Exception("Track not found")

        # If route was found, return
        return route
