import numpy as np
import networkx as nx
import copy
import math
import random



def get_node(G, ind):
    return list(G.nodes)[ind]

def find_state_population(G):
    population = 0
    for node, data in G.nodes(data = True):
        population += data['pop']

    return population

def find_unit_population(G, node):
    return G.nodes(data = True)[node]['pop']

def check_valid_weighted(G, partition, delta):
    part_populations = []
    for part in partition:
        subgrph = G.subgraph(part)
        if not nx.is_connected(subgrph):
            return False
        else:
            part_pop = 0
            for node in part:
                part_pop += G.nodes(data = True)[node]['pop']
            part_populations.append(part_pop)
    if max(part_populations) - min(part_populations) > delta:
        print(max(part_populations) - min(part_populations))
        return False
    return True

#UNFINISHED
def find_num_seats_weighted(G, partition):
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


# Generate a random valid partition:
def first_partition_weighted(G, n_district = 9, delta = 1000):
    G_copy = copy.deepcopy(G)
    partition = []
    n_dist_cur = 0

    pop_per_dist = find_state_population(G) / n_district
    # Add remaining districts:
    while n_dist_cur < n_district:
        G_copy_1 = copy.deepcopy(G_copy)
        # Choose a center for the district:
        pop_list = [[node, data['pop']] for node, data in G_copy.nodes(data = True)]
        pop_list = sorted(pop_list, key = lambda lst: -lst[1])
        district_center = pop_list[0][0]
        part = [district_center]
        district_pop = find_unit_population(G, district_center)
        G_copy_1.remove_node(district_center)

        bfs_edges = list(nx.bfs_edges(G_copy, district_center))
        bfs_iter = 0
        while district_pop < pop_per_dist - delta and bfs_iter < len(bfs_edges):
            if bfs_edges[bfs_iter][1] in G_copy_1\
                and district_pop + find_unit_population(G, bfs_edges[bfs_iter][1]) < pop_per_dist + delta:
                part.append(bfs_edges[bfs_iter][1])
                district_pop += find_unit_population(G, bfs_edges[bfs_iter][1])
                G_copy_1.remove_node(bfs_edges[bfs_iter][1])
            bfs_iter += 1

        if math.fabs(pop_per_dist - district_pop) > delta:
            print("Fail in district " + str(n_dist_cur + 1))
            return None

        partition.append(part)
        G_copy = G_copy_1
        n_dist_cur += 1

    # partition.append(list(G_copy))
    return partition

def first_partition_splitline_weighted(G, n_district = 9, delta = 1000):
    partition = []

    if n_district == 1:
        partition.append(list(G))
        return partition

    n_district_1 = np.ceil(n_district / 2)
    n_district_2 = np.floor(n_district / 2)

    pop_part_1 = n_district_1 / n_district * find_state_population(G)


    n_node_1 = n_district_1 / n_district * len(G)
    for ind in range(len(G.nodes())):
        nodes_1 = []
        nodes_2 = []
        starting_node = list(G.nodes())[ind]
        bfs_edges = list(nx.bfs_edges(G, starting_node))
        bfs_iter = 0
        nodes_1.append(starting_node)
        cur_pop = find_unit_population(G, starting_node)
        while cur_pop < pop_part_1 - delta and bfs_iter < len(bfs_edges):
            nodes_1.append(bfs_edges[bfs_iter][1])
            bfs_iter += 1
            cur_pop += find_unit_population(G, cur_pop)

        if cur_pop < pop_part_1 - delta:
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
            subpartition_1 = first_partition_splitline_weighted(G_1, n_district = n_district_1)
            subpartition_2 = first_partition_splitline_weighted(G_2, n_district = n_district_2)
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



# def add_node_bfs(G, node, n_node):
#     part = set()
#
#     return part


# UNFINISHED:
def pack_weighted(G, k, n_pack = 1):
    G_copy = copy.deepcopy(G)
    partition = []
    for node, data in G.nodes(data = True):
        data['districted'] = False
    nodes_B = [node for node, key in G.nodes(data = True) if key['party'] == -1]
    subgraph_B = nx.Graph(G.subgraph(nodes_B))
    n_dist = 0

    # Packing process
    for i in range(n_pack):
        n_pop = find_state_population(G_copy) // (k - n_dist)
        part = set()
        degrees_list = sorted(subgraph_B.degree, key = lambda tuple: tuple[1])
        district_center = degrees_list[0][0]
        part.add(district_center)
        curr_pop = find_unit_population(G, district_center)
        G.nodes(data=True)[district_center]['districted'] = True
        if n_pop > curr_pop:
            # n_ver_in_part = 1
            bfs_edges = list(nx.bfs_edges(subgraph_B, district_center))
            n_bfs = len(bfs_edges)

            bfs_iter = 0
            G_copy.remove_node(district_center)
            subgraph_B.remove_node(district_center)
            while curr_pop < n_pop and bfs_iter < n_bfs:
                while len(degrees_list) != 0 and (degrees_list[0][1] == 0) and curr_pop < n_pop:
                    if not G.nodes(data = True)[degrees_list[0][0]]['districted']:
                        part.add(degrees_list[0][0])
                        G_copy.remove_node(degrees_list[0][0])
                        subgraph_B.remove_node(degrees_list[0][0])
                        curr_pop += find_unit_population(G, degrees_list[0][0])
                        G.nodes(data=True)[degrees_list[0][0]]['districted'] = True
                    degrees_list.pop(0)
                if curr_pop < n_pop and bfs_edges[bfs_iter][1] in subgraph_B.nodes(data = False):
                    part.add(bfs_edges[bfs_iter][1])
                    G_copy.remove_node(bfs_edges[bfs_iter][1])
                    subgraph_B.remove_node(bfs_edges[bfs_iter][1])
                    degrees_list = sorted(subgraph_B.degree, key=lambda tuple: tuple[1])
                    curr_pop += find_unit_population(G, bfs_edges[bfs_iter][1])
                    G.nodes(data=True)[bfs_edges[bfs_iter][1]]['districted'] = True
                bfs_iter += 1

            # Add in extra nodes if necessary
            if curr_pop < n_pop:
                bfs_edges = list(nx.bfs_edges(G, district_center))
                bfs_iter = 0
                degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
                n_bfs = len(bfs_edges)
                while curr_pop < n_pop and bfs_iter < n_bfs:
                    while (degrees_list[0][1] == 0) and curr_pop < n_pop:
                        if not G.nodes(data = True)[degrees_list[0][0]]['districted']:
                            part.add(degrees_list[0][0])
                            G_copy.remove_node(degrees_list[0][0])
                            curr_pop += find_unit_population(G, degrees_list[0][0])
                            G.nodes(data=True)[degrees_list[0][0]]['districted'] = True
                        degrees_list.pop(0)
                    if curr_pop < n_pop and bfs_edges[bfs_iter][1] not in part:
                        part.add(bfs_edges[bfs_iter][1])
                        G_copy.remove_node(bfs_edges[bfs_iter][1])
                        degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
                        curr_pop += find_unit_population(G, bfs_edges[bfs_iter][1])
                        G.nodes(data=True)[bfs_edges[bfs_iter][1]]['districted'] = True
                    bfs_iter += 1

            if (curr_pop < n_pop):
                print("Can't redistrict")
                print(part)
                print(partition)
                return
        n_dist += 1
        partition.append(part)

    # Adding remaining districts
    for n in range(k - n_pack - 1):
        # Compute the number of vertices in the part:
        n_pop = find_state_population(G_copy) // (k - n_pack - n)

        # Compute the list of vertex, sorted in ascending order by degree:
        degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])

        # Add the vertex with the smallest degree (a corner) and its surrounding vertices using bfs:
        part = set()
        corner = degrees_list[0][0]
        part.add(corner)
        curr_pop = find_unit_population(G, corner)
        bfs_edges = list(nx.bfs_edges(G_copy, corner))
        G_copy.remove_node(corner)
        degrees_list.pop(0)
        if n_pop > curr_pop:
            i = 0
            bfs_edges_iter = 0
            n_bfs_node = len(bfs_edges)
            while curr_pop < n_pop and bfs_edges_iter < n_bfs_node:
                while (len(degrees_list) != 0 and degrees_list[0][1] == 0):
                    part.add(degrees_list[0][0])
                    G_copy.remove_node(degrees_list[0][0])
                    i += 1
                    degrees_list.pop(0)
                if (bfs_edges[bfs_edges_iter][1] not in part and curr_pop < n_pop):
                    part.add(bfs_edges[bfs_edges_iter][1])
                    G_copy.remove_node(bfs_edges[bfs_edges_iter][1])
                    degrees_list = sorted(G_copy.degree, key = lambda tuple: tuple[1])
                    i += 1
                bfs_edges_iter += 1

        # Add the part to the parts list:
        partition.append(part)

    partition.append(set(G_copy.nodes))
    return partition


def pack_weighted_v2(G, n_district = 9, n_pack = 8, delta = 1000, starting_points = None):
    G_copy = copy.deepcopy(G)
    partition = []
    n_dist_cur = 0

    pop_per_dist = find_state_population(G) / n_district

    # Packing:
    while n_dist_cur < n_pack:
        nodes_B = [node for node, data in G_copy.nodes(data=True) if data['party'] == -1]
        subgraph_B = nx.Graph(G_copy.subgraph(nodes_B))
        G_copy_1 = copy.deepcopy(G_copy)
        # Choose a starting point for the district:
        if starting_points is None:
            party_dif_list = [[node, data['party_dif']] for node, data in subgraph_B.nodes(data = True)]
            party_dif_list = np.array(sorted(party_dif_list, key = lambda lst: lst[1]))
            district_center = party_dif_list[-1][0]
        else:
            district_center = starting_points[n_dist_cur]

        district_pop = find_unit_population(G, district_center)
        part = [district_center]
        G_copy_1.remove_node(district_center)
        # Create a BFS search tree:
        bfs_edges = list(nx.bfs_edges(subgraph_B, district_center))
        bfs_iter = 0
        while pop_per_dist - district_pop > delta and bfs_iter < len(bfs_edges):
            if bfs_edges[bfs_iter][1] in G_copy_1\
                    and district_pop + find_unit_population(G, bfs_edges[bfs_iter][1]) < pop_per_dist + delta:
                part.append(bfs_edges[bfs_iter][1])
                district_pop += find_unit_population(G, bfs_edges[bfs_iter][1])
                G_copy_1.remove_node(bfs_edges[bfs_iter][1])
            bfs_iter += 1

        # Add extra nodes if neccessary:
        bfs_edges = list(nx.bfs_edges(G_copy, district_center))
        bfs_iter = 0
        while pop_per_dist - district_pop > delta and bfs_iter < len(bfs_edges):
            if bfs_edges[bfs_iter][1] in G_copy_1\
                and district_pop + find_unit_population(G, bfs_edges[bfs_iter][1]) < pop_per_dist + delta:
                part.append(bfs_edges[bfs_iter][1])
                district_pop += find_unit_population(G, bfs_edges[bfs_iter][1])
                G_copy_1.remove_node(bfs_edges[bfs_iter][1])
            bfs_iter += 1

        if math.fabs(pop_per_dist - district_pop) > delta:
            print("Fail at district " + str(n_dist_cur + 1))
            return None

        partition.append(part)
        G_copy = G_copy_1
        n_dist_cur += 1

    # Add remaining districts:
    while n_dist_cur < n_district:
        G_copy_1 = copy.deepcopy(G_copy)
        # Choose a center for the district:
        pop_list = [[node, data['pop']] for node, data in G_copy.nodes(data = True)]
        pop_list = sorted(pop_list, key = lambda lst: -lst[1])
        district_center = pop_list[0][0]
        part = [district_center]
        district_pop = find_unit_population(G, district_center)
        G_copy_1.remove_node(district_center)

        bfs_edges = list(nx.bfs_edges(G_copy, district_center))
        bfs_iter = 0
        while district_pop < pop_per_dist - delta and bfs_iter < len(bfs_edges):
            if bfs_edges[bfs_iter][1] in G_copy_1\
                and district_pop + find_unit_population(G, bfs_edges[bfs_iter][1]) < pop_per_dist + delta:
                part.append(bfs_edges[bfs_iter][1])
                district_pop += find_unit_population(G, bfs_edges[bfs_iter][1])
                G_copy_1.remove_node(bfs_edges[bfs_iter][1])
            bfs_iter += 1

        if math.fabs(pop_per_dist - district_pop) > delta:
            print("Fail in district " + str(n_dist_cur + 1))
            return None

        partition.append(part)
        G_copy = G_copy_1
        n_dist_cur += 1

    # partition.append(list(G_copy))
    return partition

# def pack_v3(G, k, n_pack, delta):
#     partition = []
#     n_dist_cur = 0
#     G_copy = copy.deepcopy(G)
#
#     return partition



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
