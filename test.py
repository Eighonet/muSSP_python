import numpy as np
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

    cost_in, cost_out = 5.0, 5.0

    transition_threshold = 0.3  # if relation strength < this threshold then it is discarded from the muSSP graph

    tracking_data = [
        [(0, 0), (10, 10), (11, 11), (20, 20), (21, 22)],
        [(14, 13), (-2, -1), (22, 21), (15, 15)],
        [(-2, -1), (10, 11), (13, 12), (24, 22)],
        [(1, 1), (12, 15), (12, 12)]
    ]

    conf = -8.8005
    confidences = [[conf for value in frame_dets] for frame_dets in tracking_data]

    objects_relations = muSSP(tracking_data, confidences,
                              cost_in, cost_out, transition_threshold, cost_function)

    tracking_data_flat = [centroid for frame_dets in tracking_data for centroid in frame_dets]

    for i, object_relations in enumerate(objects_relations):
        object_relation = sorted(
            list(set([detection_index for relation in object_relations for detection_index in relation])))
        print(f'Object {i} trajectory indexes: {object_relation}')

        print(f'Corresponding points:\n {np.array(tracking_data_flat)[object_relation]}')


if __name__ == '__main__':
    main()
