import numpy as np
import networkx as nx
import copy



def get_node(G, ind):
    return list(G.nodes)[ind]

def check_valid(G, partition):
    for part in partition:
        subgrph = G.subgraph(part)
        if not nx.is_connected(subgrph):
            return False
    return True

def find_num_seats(G, partition):
    n_seat = 0
    for part in partition:
        sum_part = 0
        for node in part:
            vote = G.nodes(data = True)[node]['party']
            sum_part += vote
        if sum_part > 0:
            n_seat += 1
        elif sum_part == 0:
            n_seat += 0.5
        # elif sum_part < 0:
        #     n_seat -= 1
    return n_seat


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

def pack(G, k, n_pack = 1):
    G_copy = copy.deepcopy(G)
    partition = []
    for node, data in G.nodes(data = True):
        data['districted'] = False
    nodes_B = [node for node, key in G.nodes(data = True) if key['party'] == -1]
    subgraph_B = nx.Graph(G.subgraph(nodes_B))
    n_dist = 0

    # Packing process
    for i in range(n_pack):
        n_ver = len(G_copy) // (k - n_dist)
        part = set()
        degrees_list = sorted(subgraph_B.degree, key = lambda tuple: tuple[1])
        district_center = degrees_list[0][0]
        part.add(district_center)
        G.nodes(data=True)[district_center]['districted'] = True
        if n_ver > 1:
            n_ver_in_part = 1
            bfs_edges = list(nx.bfs_edges(subgraph_B, district_center))
            n_bfs = len(bfs_edges)

            bfs_iter = 0
            G_copy.remove_node(district_center)
            subgraph_B.remove_node(district_center)
            while n_ver_in_part < n_ver and bfs_iter < n_bfs:
                while len(degrees_list) != 0 and (degrees_list[0][1] == 0) and n_ver_in_part < n_ver:
                    if not G.nodes(data = True)[degrees_list[0][0]]['districted']:
                        part.add(degrees_list[0][0])
                        G_copy.remove_node(degrees_list[0][0])
                        subgraph_B.remove_node(degrees_list[0][0])
                        n_ver_in_part += 1
                        G.nodes(data=True)[degrees_list[0][0]]['districted'] = True
                    degrees_list.pop(0)
                if n_ver_in_part < n_ver and bfs_edges[bfs_iter][1] in subgraph_B.nodes(data = False):
                    part.add(bfs_edges[bfs_iter][1])
                    G_copy.remove_node(bfs_edges[bfs_iter][1])
                    subgraph_B.remove_node(bfs_edges[bfs_iter][1])
                    degrees_list = sorted(subgraph_B.degree, key=lambda tuple: tuple[1])
                    n_ver_in_part += 1
                    G.nodes(data=True)[bfs_edges[bfs_iter][1]]['districted'] = True
                bfs_iter += 1

            # Add in extra nodes if necessary
            if n_ver_in_part < n_ver:
                bfs_edges = list(nx.bfs_edges(G, district_center))
                bfs_iter = 0
                degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
                n_bfs = len(bfs_edges)
                while n_ver_in_part < n_ver and bfs_iter < n_bfs:
                    while (degrees_list[0][1] == 0) and n_ver_in_part < n_ver:
                        if not G.nodes(data = True)[degrees_list[0][0]]['districted']:
                            part.add(degrees_list[0][0])
                            G_copy.remove_node(degrees_list[0][0])
                            n_ver_in_part += 1
                            G.nodes(data=True)[degrees_list[0][0]]['districted'] = True
                        degrees_list.pop(0)
                    if n_ver_in_part < n_ver and bfs_edges[bfs_iter][1] not in part:
                        part.add(bfs_edges[bfs_iter][1])
                        G_copy.remove_node(bfs_edges[bfs_iter][1])
                        degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
                        n_ver_in_part += 1
                        G.nodes(data=True)[bfs_edges[bfs_iter][1]]['districted'] = True
                    bfs_iter += 1

            if (n_ver_in_part < n_ver):
                print("Can't redistrict")
                print(part)
                print(partition)
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


def crack(G, k, n_crack):
    G_copy = copy.deepcopy(G)
    for node, key in G.nodes(data = True):
        key["districted"] = False
    check_districted = np.full(shape = (len(G_copy)), fill_value = False)
    partition = []
    nodes_A = [node for node, key in G.nodes(data = True) if key['party'] == 1]
    subgraph_A = nx.Graph(G.subgraph(nodes_A))
    n_dist = 0

    # Cracking process:
    for i in range(n_crack):
        n_ver = len(G_copy) // (k - n_dist)
        n_ver_to_win = np.ceil((n_ver + 1) / 2)
        part = set()
        degrees_list = sorted(subgraph_A.degree, key = lambda tuple: tuple[1])
        district_center = degrees_list[0][0]
        G.nodes(data=True)[district_center]['districted'] = True
        bfs_edges_A = list(nx.bfs_edges(subgraph_A, district_center))
        part.add(district_center)
        n_ver_in_part = 1

        # Filling just enough vertices to win:
        if n_ver_to_win > 1:
            n_bfs = len(bfs_edges_A)

            bfs_iter_A = 0
            G_copy.remove_node(district_center)
            subgraph_A.remove_node(district_center)

            while n_ver_in_part < n_ver_to_win and bfs_iter_A < n_bfs:
                while len(degrees_list) != 0 and (degrees_list[0][1] == 0) and n_ver_in_part < n_ver:
                    part.add(degrees_list[0][0])
                    G_copy.remove_node(degrees_list[0][0])
                    G.nodes(data = True)[degrees_list[0][0]]['districted'] = True
                    n_ver_in_part += 1
                    degrees_list.pop(0)
                if n_ver_in_part < n_ver and bfs_edges_A[bfs_iter_A][1] in subgraph_A.nodes(data = False):
                    part.add(bfs_edges_A[bfs_iter_A][1])
                    G_copy.remove_node(bfs_edges_A[bfs_iter_A][1])
                    subgraph_A.remove_node(bfs_edges_A[bfs_iter_A][1])
                    G.nodes(data=True)[bfs_edges_A[bfs_iter_A][1]]['districted'] = True
                    degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
                    n_ver_in_part += 1
                bfs_iter_A += 1

        if (n_ver_in_part < n_ver_to_win):
            print("Can't crack")
            return partition

        # Adding extra vertices from opposing party:
        if n_ver_in_part < n_ver:
            nodes_B = [node for node, key in G.nodes(data=True) if node == district_center or key['party'] == -1]
            subgraph_B = nx.Graph(G.subgraph(nodes_B))
            bfs_edges_B = list(nx.bfs_edges(subgraph_B, district_center))
            n_bfs_B = len(bfs_edges_B)
            bfs_iter_B = 0

            while n_ver_in_part < n_ver and bfs_iter_B < n_bfs_B:
                while (degrees_list[0][1] == 0) and n_ver_in_part < n_ver:
                    if not G.nodes(data=True)[degrees_list[0][0]]['districted']:
                        part.add(degrees_list[0][0])
                        G_copy.remove_node(degrees_list[0][0])
                        G.nodes(data=True)[degrees_list[0][0]]['districted'] = True
                        n_ver_in_part += 1
                    degrees_list.pop(0)
                if n_ver_in_part < n_ver and not G.nodes(data=True)[bfs_edges_B[bfs_iter_B][1]]['districted']:
                    part.add(bfs_edges_B[bfs_iter_B][1])
                    G_copy.remove_node(bfs_edges_B[bfs_iter_B][1])
                    G.nodes(data=True)[bfs_edges_B[bfs_iter_B][1]]['districted'] = True
                    degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
                    n_ver_in_part += 1
                bfs_iter_B += 1


                # G_copy.remove_node(district_center)

        # Adding extra vertices from the supported party:
        if n_ver_in_part < n_ver:
            nodes_A = [node for node, key in G.nodes(data=True) if key['party'] == 1]
            subgraph_A = nx.Graph(G.subgraph(nodes_A))
            bfs_edges_A = list(nx.bfs_edges(subgraph_A, district_center))
            n_bfs_A = len(bfs_edges_A)
            bfs_iter_A = 0

            while n_ver_in_part < n_ver and bfs_iter_A < n_bfs_A:
                while (degrees_list[0][1] == 0) and n_ver_in_part < n_ver:
                    if not G.nodes(data=True)[degrees_list[0][0]]['districted']:
                        part.add(degrees_list[0][0])
                        G_copy.remove_node(degrees_list[0][0])
                        G.nodes(data=True)[degrees_list[0][0]]['districted'] = True
                        n_ver_in_part += 1
                    degrees_list.pop(0)
                if n_ver_in_part < n_ver and not G.nodes(data=True)[bfs_edges_A[bfs_iter_A][1]]['districted']:
                    part.add(bfs_edges_A[bfs_iter_A][1])
                    G_copy.remove_node(bfs_edges_A[bfs_iter_A][1])
                    G.nodes(data=True)[bfs_edges_A[bfs_iter_A][1]]['districted'] = True
                    degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
                    n_ver_in_part += 1
                bfs_iter_A += 1

        if (n_ver_in_part < n_ver):
            print("Can't redistrict")
            return partition
        n_dist += 1
        partition.append(part)


        # If






    # Adding remaining districts
    for n in range(k - n_crack - 1):
        # Compute the number of vertices in the part:
        n_ver = len(G_copy) // (k - n_crack - n)

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





