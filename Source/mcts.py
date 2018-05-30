import numpy as np
import networkx as nx
from .gerrymandering_game import GerrymanderGame_v2
import random

class Node:

    def __init__(self, state, n_units, n_districts, parent = None, child_list = None):
        self._state = state
        self._untried_actions = []
        for position in range(n_units):
            for displacement in range(1, n_districts):
                self._untried_actions.append((position, displacement))

        self._V = 0
        self._n_visit = 0

        self._parent = parent
        if child_list is not None:
            self._child_list = child_list
        else:
            self._child_list = []


# class Tree:
#
#     def __init__(self):
#         return


class MCTS:
    def __init__(self, env, n_epochs = 100, max_tree_depth = 100, Cp = 0.7071):
        self._env = env
        self._n_epochs = n_epochs
        self._max_tree_depth = max_tree_depth
        self._Cp = Cp

    def uct_search(self, state, n_epoch_search = 10000, travarse_depth = 100):
        self._root = Node(state, n_units = self._env._n_units, n_districts = self._env._n_districts)
        for epoch in range(n_epoch_search):
            print("Epoch " + str(epoch))
            node = self.tree_policy(self._root)
            delta = self.default_policy(node._state)
            self.back_up(node = node, delta = delta)

        node_iterator = self._root
        i = 0
        while len(node_iterator._child_list) > 0 and i < travarse_depth:
            node_iterator = self.best_child(node_iterator, 0)
            i += 1

        return node_iterator._state

    def tree_policy(self, node):
        node_iterator = node
        level = 0
        while level < self._max_tree_depth:
            print("Level " + str(level))
            if len(node_iterator._untried_actions) > 0:
                return self.expand(node_iterator)
            else:
                node_iterator = self.best_child(node_iterator, self._Cp)
                level += 1

        return node_iterator

    def expand(self, node):
        act_ind = random.randrange(0, len(node._untried_actions))
        action = node._untried_actions[act_ind]
        node._untried_actions.pop(act_ind)

        new_state = self._env.act(node._state, action)
        new_node = Node(state = new_state, n_units = self._env._n_units, n_districts = self._env._n_districts, parent = node)


        node._child_list.append(new_node)
        return new_node

    def default_policy(self, state):
        state_copy = list(state)
        for _ in range(self._n_epochs):
            action = self._env.sample_action()
            state_copy = self._env.act(state_copy, action)
        return self._env.find_num_seats(state_copy)

    def back_up(self, node, delta):
        node_iterator = node
        while node_iterator is not None:
            node_iterator._n_visit += 1
            node_iterator._V += delta
            node_iterator = node_iterator._parent

    def best_child(self, node, c):
        value_list = []
        for child in node._child_list:
            value_list.append(self.score(child, c))
        return node._child_list[np.argmax(value_list)]

    def score(self, node, c):
        return node._V / node._n_visit + 2 * np.sqrt(np.log(node._parent._n_visit) / node._n_visit)

