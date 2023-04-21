import os
import math

import networkx as nx


def save_edge_list(edge_list: list, node_dict: dict) -> None:
    """
    Saves the muSSP graph + additional metadata required for tracking

    :param edge_list: extended edge list w.r.t. muSPP requirements
    :param node_dict: dictionary encoding correspondence between object numbers and nodes in the muSPP graph
    :return None
    """

    with open(os.path.dirname(__file__) + 'edge_list.txt', 'w') as f:
        f.write(f'p min {2 * len(node_dict) + 2} {len(edge_list)}\n')
        f.write(f'c min-cost flow problem with {2 * len(node_dict) + 2} nodes and {len(edge_list)} arcs\n')
        f.write('n 1          0\n')
        f.write('c supply of 1 at node          0\n')
        f.write(f'n {2 * len(node_dict) + 2}          0\n')
        f.write(f'c demand of {2 * len(node_dict) + 2} at node          0\n')
        f.write('c arc list follows\n')
        f.write('c arc has <tail> <head> <cost>\n')
        for edge in edge_list:
            f.write(f'a {edge[0]} {edge[1]} {edge[2]}\n')


def get_edge_list(tracking_data: list, confidences: list,
                  cost_in: float, cost_out: float, transition_threshold: float,
                  cost) -> tuple:
    """
    Main function for the muSPP edge list construction

    :param tracking_data: detected objects' 2D coordinates in each frame
    :param confidences: confidence list of detections (one value per coordinate pair from tracking_data)
    :param cost_in: cost of detection inclusion (specified for all detections)
    :param cost_out: cost of tracking termination (specified for all detections)
    :param transition_threshold: cost function threshold for edges addition
    :param cost: custom cost function
    :return: tuple (edge_list, node_dict)
    """

    inner_edges, terminal_edges, transition_edges = [], [], []

    upd_index_1, upd_index_2 = 0, 0

    node_dict = dict()

    for i, frame_dets in enumerate(tracking_data):
        for j, det in enumerate(frame_dets):
            inner_edges.append([upd_index_1 + 2 * j, upd_index_1 + 2 * j + 1, confidences[i][j]])
            node_dict[upd_index_2 + j] = {'in': upd_index_1 + 2 * j, 'out': upd_index_1 + 2 * j + 1}
        upd_index_1 += 2 * (len(tracking_data[i]))
        upd_index_2 += len(tracking_data[i])

    upd_index = 0
    for i, frame_dets in enumerate(tracking_data[:-1]):
        for j, det_1 in enumerate(tracking_data[i]):
            for k, det_2 in enumerate(tracking_data[i + 1]):
                edge_cost = cost(det_1, det_2)
                if edge_cost < transition_threshold:
                    transition_edges.append([node_dict[upd_index + j]['out'],
                                             node_dict[upd_index + len(tracking_data[i]) + k]['in'], -edge_cost])
        upd_index += len(tracking_data[i])

    for node in node_dict:
        terminal_edges.append([-1, node_dict[node]['in'], cost_in])

    for node in node_dict:
        terminal_edges.append([node_dict[node]['out'], 2 * len(node_dict), cost_out])

    index_shift = 2

    edge_list = terminal_edges + inner_edges + transition_edges

    for i, edge in enumerate(edge_list):
        edge[0] += index_shift
        edge[1] += index_shift
        edge_list[i] = edge

    return edge_list, node_dict


def muSSP(tracking_data: list, confidences: list,
          cost_in: float, cost_out: float, transition_threshold: float,
          cost) -> list:
    """
    Wrapper for the muSPP min-flow cost algorithm & corresponding graph construction

    :param tracking_data: detected objects' 2D coordinates in each frame
    :param confidences: confidence list of detections (one value per coordinate pair from tracking_data)
    :param cost_in: cost of detection inclusion (specified for all detections)
    :param cost_out: cost of tracking termination (specified for all detections)
    :param transition_threshold: cost function threshold for edges addition
    :param cost: custom cost function
    :return: list of relations between detected objects
    """

    edge_list, node_dict = get_edge_list(tracking_data, confidences, cost_in, cost_out, transition_threshold, cost)
    save_edge_list(edge_list, node_dict)

    os.system(os.path.dirname(__file__) + "/muSSP/muSSP/muSSP edge_list.txt")

    with open('output.txt', 'r') as f:
        output = f.read().split('\n')[:-1]
        output = [edge.split(' ')[1:3] for edge in output if edge[-1] == '1']

    G = nx.Graph(output)
    G.remove_node('1')
    G.remove_node(str(2 * len(node_dict) + 2))

    paths = [c for c in nx.connected_components(G)]

    trj_edges = []
    for path in paths:
        trj_edges.append(list(G.subgraph(path).edges))

    edges_filtered = [[sorted([int(math.floor(int(edge[0]) / 2)) - 1, int(math.floor(int(edge[1]) / 2)) - 1])
                       for edge in trj if (math.floor(int(edge[0]) / 2) != math.floor(int(edge[1]) / 2))]
                      for trj in trj_edges]

    return [sorted(edges) for edges in edges_filtered]
