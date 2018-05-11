import numpy as np
import networkx as nx
import copy



def get_node(G, ind):
    return list(G.nodes)[ind]


def first_partition(G, k):
    parts_list = []
    G_copy = copy.deepcopy(G)
    for n in range(k-1):
        # Compute the number of vertices in the part:
        n_ver = len(G_copy) // (k - n)

        # Compute the list of vertex, sorted in ascending order by degree:
        degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])

        # Add the vertex with the smallest degree (a corner) and its surrounding vertices using bfs:
        part = [degrees_list[0][0]]
        bfs_edges = list(nx.bfs_edges(G_copy, degrees_list[0][0]))
        if n_ver > 1:
            for i in range(n_ver - 1):
                part.append(bfs_edges[i][1])

        # Add the part to the parts list:
        parts_list.append(part)

        # Remove the added vertices from the graph:
        G_copy.remove_nodes_from(part)

    parts_list.append(list(G_copy.nodes))

    return parts_list


# model_graph = nx.Graph()
# model_graph.add_nodes_from([0, 1, 2, 3, 4])
# model_graph.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (0, 1), (0, 2), (0, 3), (0, 4)])


# print(5 // 4)
# print(first_partition(model_graph, 3))
# print(list(model_graph))

# model_graph_1 = nx.Graph()
# model_graph_1.add_nodes_from([0, 1, 2, 3])
# model_graph_1.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 3)])
# print(list(nx.bfs_edges(model_graph_1, 0)))
