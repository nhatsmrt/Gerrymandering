import numpy as np
import networkx as nx
import copy
import random


# class GerrymanderGame():
#
#     def __init__(self, G, n_districts, n_units, partition = None, state = None, seed = 0):
#         self._n_districts = n_districts
#         self._n_units = n_units
#         self._G = G
#         if state is not None:
#             self._state = state
#         else:
#             if partition is not None:
#                 self._state = self.partition_to_state(partition)
#             else:
#                 self._state = self.partition_to_state(self.first_partition())
#         random.seed(seed)
#
#     def act_on_current_state(self, action):
#         old_state = list(self._state)
#         new_state = list(self._state)
#         new_state[int(action[0])] = (new_state[int(action[0])] + action[1]) % self._n_districts
#         self._state = new_state
#         return new_state, self.reward(old_state, action)
#
#     def act(self, state, action, one_hot = False):
#         new_state = list(state)
#         new_state[int(action[0])] = (new_state[int(action[0])] + action[1]) % self._n_districts
#         if one_hot:
#             new_state = self.one_hot_state(new_state)
#         return new_state, self.reward(state, action)
#
#
#     def sample_action(self):
#         position = random.randrange(0, self._n_units)
#         displacement = random.randrange(1, self._n_districts)
#         return (position, displacement)
#
#     def sample_state(self, one_hot = False):
#         state = []
#         for _ in range(self._n_units):
#             state.append(random.randrange(0, self._n_districts))
#         if one_hot:
#             return self.one_hot_state(state)
#         return state
#
#     def check_valid(self, partition, epsilon_size = 1):
#
#         # Check number of parts:
#         n_part = len(partition)
#         if n_part != self._n_districts:
#             return False
#
#         # Check if any part is empty:
#         for part in partition:
#             if not bool(part):
#                 return False
#
#         # Check the size of the partitions
#         parts_size = [len(part) for part in partition]
#         parts_size_min = min(parts_size)
#         parts_size_max = max(parts_size)
#         if parts_size_max - parts_size_min > epsilon_size:
#             return False
#
#         # Compute the number of districts (seats) won:
#         for part in partition:
#             subgrph = self._G.subgraph(part)
#             if not nx.is_connected(subgrph):
#                 return False
#         return True
#
#     def find_num_seats(self, partition):
#         # Punishing heavily illegal partitions
#         if not self.check_valid(partition):
#             return -10
#
#         # Counting the number of seats:
#         n_seat = 0
#         for part in partition:
#             sum_part = 0
#             for node in part:
#                 vote = self._G.nodes(data=True)[node]['party']
#                 sum_part += vote
#             if sum_part > 0:
#                 n_seat += 1
#             elif sum_part == 0:
#                 n_seat += 0.5
#                 # elif sum_part < 0:
#                 #     n_seat -= 1
#         return n_seat
#
#     def state_to_partition(self, state):
#         partition = [set() for i in range(self._n_districts)]
#         for i in range(len(state)):
#             partition[int(state[i])].add(i)
#         return partition
#
#     def partition_to_state(self, partition):
#         state = [0 for _ in range(self._n_units)]
#         for i in range(len(partition)):
#             for node in partition[i]:
#                 state[node] = i
#
#         return state
#
#     def first_partition(self):
#         parts_list = []
#         G_copy = copy.deepcopy(self._G)
#         for n in range(self._n_districts - 1):
#             # Compute the number of vertices in the part:
#             n_ver = len(G_copy) // (self._n_districts - n)
#
#             # Compute the list of vertex, sorted in ascending order by degree:
#             degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
#
#             # Add the vertex with the smallest degree (a corner) and its surrounding vertices using bfs:
#             part = set()
#             part.add(degrees_list[0][0])
#             bfs_edges = list(nx.bfs_edges(G_copy, degrees_list[0][0]))
#             G_copy.remove_node(degrees_list[0][0])
#             degrees_list.pop(0)
#             if n_ver > 1:
#                 i = 0
#                 bfs_edges_iter = 0
#                 n_bfs_node = len(bfs_edges)
#                 while i < n_ver - 1 and bfs_edges_iter < n_bfs_node:
#                     while (degrees_list[0][1] == 0 and degrees_list != 0):
#                         part.add(degrees_list[0][0])
#                         G_copy.remove_node(degrees_list[0][0])
#                         i += 1
#                         degrees_list.pop(0)
#                     if (bfs_edges[bfs_edges_iter][1] not in part and i < n_ver - 1):
#                         part.add(bfs_edges[bfs_edges_iter][1])
#                         G_copy.remove_node(bfs_edges[bfs_edges_iter][1])
#                         degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
#                         i += 1
#                     bfs_edges_iter += 1
#
#             # Add the part to the parts list:
#             parts_list.append(part)
#
#         parts_list.append(set(G_copy.nodes))
#
#         return parts_list
#
#     def one_hot_state(self, state):
#         oh_state = np.zeros(shape = [self._n_units, self._n_districts])
#         ind_row = [i for i in range(len(state))]
#         ind_col = [state[i] for i in range(len(state))]
#         oh_state[ind_row, ind_col] = 1
#         return oh_state
#
#     def reward(self, state, action):
#         partition_old = self.state_to_partition(state)
#
#         new_state = list(state)
#         print(action)
#         new_state[int(action[0])] = (new_state[int(action[0])] + action[1]) % self._n_districts
#         partition_new = self.state_to_partition(new_state)
#
#
#
#         return self.find_num_seats(partition_new) - self.find_num_seats(partition_old)
#
class GerrymanderGame_v2():

    def __init__(self, G, n_districts, n_units, partition = None, state = None, seed = 0):
        self._n_districts = n_districts
        self._n_units = n_units
        self._G = G
        if state is not None:
            self._state = state
        else:
            if partition is not None:
                self._state = self.partition_to_state(partition)
            else:
                self._state = self.partition_to_state(self.first_partition())
        random.seed(seed)

    def act_on_current_state(self, action):
        old_state = np.array(self._state)
        new_state = np.array(self._state)
        curr_pos = np.argmax(new_state[int(action[0])])
        new_pos = (curr_pos + action[1]) % 2
        new_state[int(action[0])] = np.zeros(self._n_districts)
        new_state[int(action[0])][new_pos] = 1
        self._state = new_state
        return new_state, self.reward(old_state, action)

    def act(self, state, action, compute_reward = True):
        new_state = np.array(state)
        curr_pos = np.argmax(new_state[int(action[0])])
        new_pos = (curr_pos + action[1]) % 2
        new_state[int(action[0])] = np.zeros(self._n_districts)
        new_state[int(action[0])][new_pos] = 1
        return new_state


    def sample_action(self):
        position = random.randrange(0, self._n_units)
        displacement = random.randrange(1, self._n_districts)
        return (position, displacement)

    def sample_state(self):
        state = np.zeros(shape = [self._n_units, self._n_districts])
        for _ in range(self._n_units):
            ind = random.randrange(0, self._n_districts)
            state[ind] = 1
        return state

    def check_valid(self, partition, epsilon_size = 1):

        # Check number of parts:
        n_part = len(partition)
        if n_part != self._n_districts:
            return False

        # Check if any part is empty:
        for part in partition:
            if not bool(part):
                return False

        # Check the size of the partitions
        parts_size = [len(part) for part in partition]
        parts_size_min = min(parts_size)
        parts_size_max = max(parts_size)
        if parts_size_max - parts_size_min > epsilon_size:
            return False

        # Compute the number of districts (seats) won:
        for part in partition:
            subgrph = self._G.subgraph(part)
            if not nx.is_connected(subgrph):
                return False
        return True

    def find_num_seats(self, partition):
        # Punishing heavily illegal partitions
        if not self.check_valid(partition):
            return -10

        # Counting the number of seats:
        n_seat = 0
        for part in partition:
            sum_part = 0
            for node in part:
                vote = self._G.nodes(data=True)[node]['party']
                sum_part += vote
            if sum_part > 0:
                n_seat += 1
            elif sum_part == 0:
                n_seat += 0.5
                # elif sum_part < 0:
                #     n_seat -= 1
        return n_seat

    def state_to_partition(self, state):
        partition = [set() for i in range(self._n_districts)]
        for node in range(state.shape[0]):
            part_ind = np.argmax(state[node])
            partition[part_ind].add(node)
        return partition

    def partition_to_state(self, partition):
        state = np.zeros(shape = [self._n_units, self._n_districts])
        for i in range(len(partition)):
            for node in partition[i]:
                state[node][i] = 1

        return state

    def first_partition(self):
        parts_list = []
        G_copy = copy.deepcopy(self._G)
        for n in range(self._n_districts - 1):
            # Compute the number of vertices in the part:
            n_ver = len(G_copy) // (self._n_districts - n)

            # Compute the list of vertex, sorted in ascending order by degree:
            degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])

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
                        degrees_list = sorted(G_copy.degree, key=lambda tuple: tuple[1])
                        i += 1
                    bfs_edges_iter += 1

            # Add the part to the parts list:
            parts_list.append(part)

        parts_list.append(set(G_copy.nodes))

        return parts_list


    def reward(self, state, action):
        partition_old = self.state_to_partition(state)

        new_state = self.act(state, action)
        partition_new = self.state_to_partition(new_state)


        return self.find_num_seats(partition_new) - self.find_num_seats(partition_old)


