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


# Generate a random valid partition
def first_partition(G, k):
    parts_list = []
    G_copy = copy.deepcopy(G)
    for n in range(k - 1):
        # Compute the number of vertices in the part:
        n_ver = len(G_copy) // (k - n)

        # Compute the list of vertex, sorted in ascending order by degree:
        degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])

        # Add the vertex with the smallest degree (a corner) and its surrounding vertices using bfs:
        part = set()
        part.add(degrees_list[0][0])
        bfs_edges = list(nx.bfs_edges(G_copy, degrees_list[0][0]))
        G_copy.remove_node(degrees_list[0][0])
        degrees_list.pop(0)
        if n_ver > 1:
            i = 0
            bfs_edges_iter = 0
            n_bfs_node = len(bfs_edges)
            while i < n_ver - 1 and bfs_edges_iter < n_bfs_node:
                while (degrees_list[0][1] == 0 and degrees_list != 0):
                    part.add(degrees_list[0][0])
                    G_copy.remove_node(degrees_list[0][0])
                    i += 1
                    degrees_list.pop(0)
                if (bfs_edges[bfs_edges_iter][1] not in part and i < n_ver - 1):
                    part.add(bfs_edges[bfs_edges_iter][1])
                    G_copy.remove_node(bfs_edges[bfs_edges_iter][1])
                    degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])
                    i += 1
                bfs_edges_iter += 1

        # Add the part to the parts list:
        parts_list.append(part)


    parts_list.append(set(G_copy.nodes))

    return parts_list


# def add_node_bfs(G, node, n_node):
#     part = set()
#
#     return part


def pack_then_crack(G, k, n_pack = 1):
    G_copy = copy.deepcopy(G)
    partition = []
    nodes_B = [node for node, key in G.nodes(data = True) if key['party'] == -1]
    subgraph_B = nx.Graph(G.subgraph(nodes_B))
    n_dist = 0

    # Packing process
    for i in range(n_pack):
        n_ver = len(G_copy) // (k - n_dist)
        part = set()
        degrees_list = sorted(subgraph_B.degree, key = lambda tuple: tuple[1])
        district_center = degrees_list[-1][0]
        part.add(district_center)
        if n_ver > 1:
            n_ver_in_part = 1
            bfs_edges = list(nx.bfs_edges(subgraph_B, district_center))
            n_bfs = len(bfs_edges)

            bfs_iter = 0
            G_copy.remove_node(district_center)
            subgraph_B.remove_node(district_center)
            while n_ver_in_part < n_ver and bfs_iter < n_bfs:
                while len(degrees_list) != 0 and (degrees_list[0][1] == 0) and n_ver_in_part < n_ver:
                    part.add(degrees_list[0][0])
                    G_copy.remove_node(degrees_list[0][0])
                    subgraph_B.remove_node(degrees_list[0][0])
                    n_ver_in_part += 1
                    degrees_list.pop(0)
                if n_ver_in_part < n_ver and bfs_edges[bfs_iter][1] in subgraph_B.nodes(data = False):
                    part.add(bfs_edges[bfs_iter][1])
                    G_copy.remove_node(bfs_edges[bfs_iter][1])
                    subgraph_B.remove_node(bfs_edges[bfs_iter][1])
                    degrees_list = sorted(subgraph_B.degree, key=lambda tuple: tuple[1])
                    n_ver_in_part += 1
                bfs_iter += 1

            if n_ver_in_part < n_ver:
                bfs_edges = list(nx.bfs_edges(G_copy, district_center))
                bfs_iter = 0
                degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
                while n_ver_in_part < n_ver and bfs_iter < n_bfs:
                    while (degrees_list[0][1] == 0) and n_ver_in_part < n_ver:
                        part.add(degrees_list[0][0])
                        G_copy.remove_node(degrees_list[0][0])
                        n_ver_in_part += 1
                        degrees_list.pop(0)
                    if n_ver_in_part < n_ver and bfs_edges[bfs_iter][1] not in part:
                        part.add(bfs_edges[bfs_iter][1])
                        G_copy.remove_node(bfs_edges[bfs_iter][1])
                        degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
                        n_ver_in_part += 1
                    bfs_iter += 1

            if (n_ver_in_part < n_ver):
                print("Can't redistrict")
                return
        n_dist += 1
        partition.append(part)

    # Adding remaining districts
    for n in range(k - n_pack - 1):
        # Compute the number of vertices in the part:
        n_ver = len(G_copy) // (k - n_pack - n)

        # Compute the list of vertex, sorted in ascending order by degree:
        degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])

        # Add the vertex with the smallest degree (a corner) and its surrounding vertices using bfs:
        part = set()
        part.add(degrees_list[0][0])
        bfs_edges = list(nx.bfs_edges(G_copy, degrees_list[0][0]))
        G_copy.remove_node(degrees_list[0][0])
        degrees_list.pop(0)
        if n_ver > 1:
            i = 0
            bfs_edges_iter = 0
            n_bfs_node = len(bfs_edges)
            while i < n_ver - 1 and bfs_edges_iter < n_bfs_node:
                while (len(degrees_list) != 0 and degrees_list[0][1] == 0):
                    part.add(degrees_list[0][0])
                    G_copy.remove_node(degrees_list[0][0])
                    i += 1
                    degrees_list.pop(0)
                if (bfs_edges[bfs_edges_iter][1] not in part and i < n_ver - 1):
                    part.add(bfs_edges[bfs_edges_iter][1])
                    G_copy.remove_node(bfs_edges[bfs_edges_iter][1])
                    degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])
                    i += 1
                bfs_edges_iter += 1

        # Add the part to the parts list:
        partition.append(part)

    partition.append(set(G_copy.nodes))
    return partition




model_graph = nx.Graph()
model_graph.add_nodes_from([0, 1, 2, 3, 4])
model_graph.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (0, 1), (0, 2), (0, 3), (0, 4)])
party_support = {0: {'party' : 1}, 1: {'party' : -1}, 2: {'party' : -1}, 3: {'party' : -1}, 4: {'party' : 1}}
nx.set_node_attributes(model_graph, party_support)

party_support_2 = dict()

model_graph_2 = nx.Graph()
for i in range(17):
    model_graph_2.add_node(i)
    if (i < 12):
        party_support_2[i] = {'party': -1}
    else:
        party_support_2[i] = {'party': 1}

for i in range(4):
    model_graph_2.add_edge(i * 4 + 0, i * 4 + 1)
    model_graph_2.add_edge(i * 4 + 1, i * 4 + 2)
    model_graph_2.add_edge(i * 4 + 2, i * 4 + 3)
    model_graph_2.add_edge(i * 4 + 3, i * 4 + 0)

model_graph_2.add_edge(16, 0)
model_graph_2.add_edge(16, 4)
model_graph_2.add_edge(16, 8)
model_graph_2.add_edge(16, 12)
nx.set_node_attributes(model_graph_2, party_support_2)


print(first_partition(model_graph, k = 2))
print(pack_then_crack(model_graph, k = 2))
print(pack_then_crack(model_graph_2, k = 4, n_pack = 2))
print(first_partition(model_graph_2, 4))
print(check_valid(model_graph_2, first_partition(model_graph_2, 4)))
print(check_valid(model_graph, first_partition(model_graph, k = 2)))



