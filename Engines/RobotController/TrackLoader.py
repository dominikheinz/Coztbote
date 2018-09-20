class TrackLoader:

    street_map = {
        (0, 1): ['L', 'R', 'L'],
        (0, 2): ['S'],
        (0, 3): ['L', 'R'],
        (0, 4): ['L', 'S', 'L'],
        (0, 5): ['L', 'S', 'S']

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

