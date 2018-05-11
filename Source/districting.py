import numpy as np
import networkx as nx
import copy



def get_node(G, ind):
    return list(G.nodes)[ind]

def check_valid(G, parts_list):
    for part in parts_list:
        subgrph = G.subgraph(part)
        if not nx.is_connected(subgrph):
            return False
    return True


# def first_partition(G, k):
#     parts_list = []
#     G_copy = copy.deepcopy(G)
#     for n in range(k-1):
#         # Compute the number of vertices in the part:
#         n_ver = len(G_copy) // (k - n)
#
#         # Compute the list of vertex, sorted in ascending order by degree:
#         degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])
#
#         # Add the vertex with the smallest degree (a corner) and its surrounding vertices using bfs:
#         part = [degrees_list[0][0]]
#         bfs_edges = list(nx.bfs_edges(G_copy, degrees_list[0][0]))
#         G_copy.remove_node(degrees_list[0][0])
#         if n_ver > 1:
#             # print(bfs_edges)
#             for i in range(n_ver - 1):
#                 degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
#                 if degrees_list[0][1] == 0:
#                     part.append(degrees_list[0][0])
#                     G_copy.remove_node(degrees_list[0][0])
#                 else:
#                     part.append(bfs_edges[i][1])
#                     G_copy.remove_node(bfs_edges[i][1])
#
#         # Add the part to the parts list:
#         parts_list.append(part)
#
#
#     parts_list.append(list(G_copy.nodes))
#
#     return parts_list

def first_partition(G, k):
    parts_list = []
    G_copy = copy.deepcopy(G)
    for n in range(k-1):
        # Compute the number of vertices in the part:
        n_ver = len(G_copy) // (k - n)

        # Compute the list of vertex, sorted in ascending order by degree:
        degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])

        # Add the vertex with the smallest degree (a corner) and its surrounding vertices using bfs:
        part = set()
        part.add(degrees_list[0][0])
        bfs_edges = list(nx.bfs_edges(G_copy, degrees_list[0][0]))
        G_copy.remove_node(degrees_list[0][0])
        degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
        if n_ver > 1:
            # print(bfs_edges)
            i = 0
            bfs_edges_iter = 0
            n_bfs_node = len(bfs_edges)
            while i < n_ver - 1 and bfs_edges_iter < n_bfs_node:
                while (degrees_list[0][1] == 0):
                    part.add(degrees_list[0][0])
                    G_copy.remove_node(degrees_list[0][0])
                    i += 1
                    degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])
                if (bfs_edges[bfs_edges_iter][1] not in part):
                    part.add(bfs_edges[bfs_edges_iter][1])
                    G_copy.remove_node(bfs_edges[bfs_edges_iter][1])
                    degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])
                    i += 1
                bfs_edges_iter += 1

        # Add the part to the parts list:
        parts_list.append(part)


    parts_list.append(set(G_copy.nodes))

    return parts_list



model_graph = nx.Graph()
model_graph.add_nodes_from([0, 1, 2, 3, 4])
model_graph.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (0, 1), (0, 2), (0, 3), (0, 4)])

model_graph_2 = nx.Graph()
for i in range(17):
    model_graph_2.add_node(i)
for i in range(4):
    model_graph_2.add_edge(i * 4 + 0, i * 4 + 1)
    model_graph_2.add_edge(i * 4 + 1, i * 4 + 2)
    model_graph_2.add_edge(i * 4 + 2, i * 4 + 3)
    model_graph_2.add_edge(i * 4 + 3, i * 4 + 0)

model_graph_2.add_edge(16, 0)
model_graph_2.add_edge(16, 4)
model_graph_2.add_edge(16, 8)
model_graph_2.add_edge(16, 12)

print(first_partition(model_graph, 2))
print(check_valid(model_graph_2, first_partition(model_graph_2, 4)))



