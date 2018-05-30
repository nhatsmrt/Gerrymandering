import numpy as np
import networkx as nx
import copy



def get_node(G, ind):
    return list(G.nodes)[ind]

def check_valid(G, partition):
    for part in partition:
        subgrph = G.subgraph(part)
        if not nx.is_connected(subgrph):
            print(part)
            return False
    return True

def find_corner(G, n_corner = 9):
    return [sorted(G.degree, key = lambda tuple: tuple[1])[i][0] for i in range(n_corner)]

def find_corner_closeness(G, n_corner = 9):
    closeness_centrality_dict = nx.closeness_centrality(G)
    center = sorted(closeness_centrality_dict, key = closeness_centrality_dict.get)[-1]
    distances = nx.shortest_path_length(G, source = center)
    return sorted(distances, key = distances.get)[-n_corner:]

def find_corner_betweenness(G, n_corner = 9):
    closeness_centrality_dict = nx.betweenness_centrality(G)
    center = sorted(closeness_centrality_dict, key = closeness_centrality_dict.get)[-1]
    distances = nx.shortest_path_length(G, source = center)
    return sorted(distances, key = distances.get)[-n_corner:]

def find_corner_katz(G, n_corner = 9):
    closeness_centrality_dict = nx.katz_centrality(G)
    center = sorted(closeness_centrality_dict, key = closeness_centrality_dict.get)[-1]
    distances = nx.shortest_path_length(G, source = center)
    return sorted(distances, key = distances.get)[-n_corner:]


def district_size(n_vertices, n_district):
    size_list = []
    for i in range(n_district):
        size_list.append(np.floor(n_vertices * (i + 1) / n_district + 0.5) - np.floor(n_vertices * (i) / n_district + 0.5))
    return size_list

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
def first_partition(G, k, delta = 5):
    parts_list = []
    G_copy = copy.deepcopy(G)
    size_list = district_size(len(G), n_district = k)
    n = 0
    while n < k - 1 or len(G_copy) == 0:
        # Compute the number of vertices in the part:
        # n_ver = district_size(len(G_copy), n_district = k - n)[0]
        n_ver = size_list[n]

        # Compute the list of vertex, sorted in ascending order by degree:
        degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])

        # Add the vertex with the smallest degree (a corner) and its surrounding vertices using bfs:
        part = []
        part.append(degrees_list[0][0])
        bfs_edges = list(nx.bfs_edges(G_copy, degrees_list[0][0]))
        G_copy.remove_node(degrees_list[0][0])
        degrees_list.pop(0)
        if n_ver > 1:
            i = 0
            bfs_edges_iter = 0
            n_bfs_node = len(bfs_edges)
            while i < n_ver - 1 and bfs_edges_iter < n_bfs_node:
                while len(degrees_list) > 0 and degrees_list[0][1] == 0 and degrees_list != 0 and i < n_ver - 1:
                    part.append(degrees_list[0][0])
                    G_copy.remove_node(degrees_list[0][0])
                    i += 1
                    degrees_list.pop(0)
                if (bfs_edges[bfs_edges_iter][1] not in part and i < n_ver - 1):
                    part.append(bfs_edges[bfs_edges_iter][1])
                    G_copy.remove_node(bfs_edges[bfs_edges_iter][1])
                    degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])
                    i += 1
                bfs_edges_iter += 1

        # Add the part to the parts list:
        if len(part) < n_ver - delta:
            if len(part) > delta:
                print("Can't district")
                print(part)
                return None
            else:
                for part_finished in parts_list:
                    if nx.has_path(G, part[0], part_finished[0]):
                        for ind in range(len(part)):
                            part_finished.append(part[ind])
                        break

        else:
            parts_list.append(part)
            n += 1


    parts_list.append(list(G_copy.nodes))

    return parts_list

def first_partition_v2(G, n_district = 9, delta = 5, starting_list = None):
    if starting_list is None:
        corners = find_corner_closeness(G, n_corner = n_district)
    else:
        corners = starting_list
    G_copy = copy.deepcopy(G)
    partition = [[corner] for corner in corners]
    G_copy.remove_nodes_from([corner for corner in corners])
    while len(G_copy) > 0:
        # print(partition)
        for i in range(n_district):
            bfs_edges = list(nx.bfs_edges(G, corners[i]))
            bfs_iter = 0
            added = False
            while bfs_iter < len(bfs_edges) and not added:
                if bfs_edges[bfs_iter][1] in list(G_copy):
                    part_temp = list(partition[i])
                    part_temp.append(bfs_edges[bfs_iter][1])
                    if nx.is_connected(nx.subgraph(G, part_temp)):
                        G_copy.remove_node(bfs_edges[bfs_iter][1])
                        partition[i].append(bfs_edges[bfs_iter][1])
                        added = True
                    else:
                        bfs_iter += 1
                else:
                    bfs_iter += 1


    return partition

def first_partition_splitline(G, n_district):
    partition = []

    if n_district == 1:
        partition.append(list(G))
        return partition

    n_district_1 = np.ceil(n_district / 2)
    n_district_2 = np.floor(n_district / 2)


    n_node_1 = n_district_1 / n_district * len(G)
    corners = find_corner(G, len(G))
    for ind in range(len(G.nodes())):
        nodes_1 = []
        nodes_2 = []
        starting_node = corners[ind]
        bfs_edges = list(nx.bfs_edges(G, starting_node))
        bfs_iter = 0
        nodes_1.append(starting_node)
        n_node_cur = 1
        while n_node_cur < n_node_1 and bfs_iter < len(bfs_edges):
            nodes_1.append(bfs_edges[bfs_iter][1])
            bfs_iter += 1
            n_node_cur += 1

        if n_node_cur < n_node_1:
            if ind == len(G.nodes()) - 1:
                print("Fail at " + str(n_district))
                return None
            else:
                continue

        for node in G.nodes():
            if node not in nodes_1:
                nodes_2.append(node)

        if (nx.is_connected(G.subgraph(nodes_2))):
            G_1 = nx.Graph(G.subgraph(nodes_1))
            G_2 = nx.Graph(G.subgraph(nodes_2))
            subpartition_1 = first_partition_splitline(G_1, n_district = n_district_1)
            subpartition_2 = first_partition_splitline(G_2, n_district = n_district_2)
            if subpartition_1 is None:
                continue
            elif subpartition_2 is None:
                continue
            else:
                for part in subpartition_1:
                    partition.append(part)

                for part in subpartition_2:
                    partition.append(part)

        elif ind == len(G.nodes()) - 1:
            print("Fail at " + str(n_district))
            print("Type 2")
            return None

    return partition




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
        part = list()
        degrees_list = sorted(subgraph_B.degree, key = lambda tuple: tuple[1])
        district_center = degrees_list[0][0]
        part.append(district_center)
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
                        part.append(degrees_list[0][0])
                        G_copy.remove_node(degrees_list[0][0])
                        subgraph_B.remove_node(degrees_list[0][0])
                        n_ver_in_part += 1
                        G.nodes(data=True)[degrees_list[0][0]]['districted'] = True
                    degrees_list.pop(0)
                if n_ver_in_part < n_ver and bfs_edges[bfs_iter][1] in subgraph_B.nodes(data = False) and bfs_edges[bfs_iter][1] in G_copy:
                    part.append(bfs_edges[bfs_iter][1])
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
                            part.append(degrees_list[0][0])
                            G_copy.remove_node(degrees_list[0][0])
                            n_ver_in_part += 1
                            G.nodes(data=True)[degrees_list[0][0]]['districted'] = True
                        degrees_list.pop(0)
                    if n_ver_in_part < n_ver and bfs_edges[bfs_iter][1] not in part and bfs_edges[bfs_iter][1] in G_copy:
                        part.append(bfs_edges[bfs_iter][1])
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
        part = list()
        part.append(degrees_list[0][0])
        bfs_edges = list(nx.bfs_edges(G_copy, degrees_list[0][0]))
        G_copy.remove_node(degrees_list[0][0])
        degrees_list.pop(0)
        if n_ver > 1:
            i = 0
            bfs_edges_iter = 0
            n_bfs_node = len(bfs_edges)
            while i < n_ver - 1 and bfs_edges_iter < n_bfs_node:
                while (len(degrees_list) != 0 and degrees_list[0][1] == 0):
                    part.append(degrees_list[0][0])
                    G_copy.remove_node(degrees_list[0][0])
                    i += 1
                    degrees_list.pop(0)
                if (bfs_edges[bfs_edges_iter][1] not in part and i < n_ver - 1):
                    part.append(bfs_edges[bfs_edges_iter][1])
                    G_copy.remove_node(bfs_edges[bfs_edges_iter][1])
                    degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])
                    i += 1
                bfs_edges_iter += 1

        # Add the part to the parts list:
        partition.append(part)

    partition.append(list(G_copy.nodes))
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
        part = list()
        degrees_list = sorted(subgraph_A.degree, key = lambda tuple: tuple[1])
        district_center = degrees_list[0][0]
        G.nodes(data=True)[district_center]['districted'] = True
        bfs_edges_A = list(nx.bfs_edges(subgraph_A, district_center))
        part.append(district_center)
        n_ver_in_part = 1

        # Filling just enough vertices to win:
        if n_ver_to_win > 1:
            n_bfs = len(bfs_edges_A)

            bfs_iter_A = 0
            G_copy.remove_node(district_center)
            subgraph_A.remove_node(district_center)

            while n_ver_in_part < n_ver_to_win and bfs_iter_A < n_bfs:
                while len(degrees_list) != 0 and (degrees_list[0][1] == 0) and n_ver_in_part < n_ver:
                    part.append(degrees_list[0][0])
                    G_copy.remove_node(degrees_list[0][0])
                    G.nodes(data = True)[degrees_list[0][0]]['districted'] = True
                    n_ver_in_part += 1
                    degrees_list.pop(0)
                if n_ver_in_part < n_ver and bfs_edges_A[bfs_iter_A][1] in subgraph_A.nodes(data = False):
                    part.append(bfs_edges_A[bfs_iter_A][1])
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
                        part.append(degrees_list[0][0])
                        G_copy.remove_node(degrees_list[0][0])
                        G.nodes(data=True)[degrees_list[0][0]]['districted'] = True
                        n_ver_in_part += 1
                    degrees_list.pop(0)
                if n_ver_in_part < n_ver and not G.nodes(data=True)[bfs_edges_B[bfs_iter_B][1]]['districted']:
                    part.append(bfs_edges_B[bfs_iter_B][1])
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
                        part.append(degrees_list[0][0])
                        G_copy.remove_node(degrees_list[0][0])
                        G.nodes(data=True)[degrees_list[0][0]]['districted'] = True
                        n_ver_in_part += 1
                    degrees_list.pop(0)
                if n_ver_in_part < n_ver and not G.nodes(data=True)[bfs_edges_A[bfs_iter_A][1]]['districted']:
                    part.append(bfs_edges_A[bfs_iter_A][1])
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
        part = list()
        part.append(degrees_list[0][0])
        bfs_edges = list(nx.bfs_edges(G_copy, degrees_list[0][0]))
        G_copy.remove_node(degrees_list[0][0])
        degrees_list.pop(0)
        if n_ver > 1:
            i = 0
            bfs_edges_iter = 0
            n_bfs_node = len(bfs_edges)
            while i < n_ver - 1 and bfs_edges_iter < n_bfs_node:
                while (len(degrees_list) != 0 and degrees_list[0][1] == 0):
                    part.append(degrees_list[0][0])
                    G_copy.remove_node(degrees_list[0][0])
                    i += 1
                    degrees_list.pop(0)
                if (bfs_edges[bfs_edges_iter][1] not in part and i < n_ver - 1):
                    part.append(bfs_edges[bfs_edges_iter][1])
                    G_copy.remove_node(bfs_edges[bfs_edges_iter][1])
                    degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])
                    i += 1
                bfs_edges_iter += 1

        # Add the part to the parts list:
        partition.append(part)

    partition.append(list(G_copy.nodes))
    return partition





