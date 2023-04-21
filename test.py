from muSSP import muSSP


def main():
    def cost_function(point_1: list, point_2: list) -> float:
        """
        Example of a possible cost function for the muSSP graph construction
        (should be replaced)

        :param point_1: 2D coordinate of the first detection
        :param point_2: 2D coordinate of the second detection
        :return: float
        """

        return 5 / (((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2) ** 0.5 + 1)

    conf = -8.8005
    confidences = [[conf for value in frame_dets] for frame_dets in tracking_data]

    cost_in, cost_out = 5.0, 5.0

    transition_threshold = 10.75

    tracking_data = [
        [(0, 0), (10, 10), (11, 11), (20, 20), (21, 22)],
        [(-2, -1), (14, 13), (15, 15), (22, 21)],
        [(-2, -1), (10, 11), (13, 12), (24, 22)]
    ]

    objects_relations = muSSP(tracking_data, confidences,
                              cost_in, cost_out, transition_threshold, cost_function)
    print(objects_relations)


if __name__ == '__main__':
    main()
