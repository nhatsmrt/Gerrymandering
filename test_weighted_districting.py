import numpy as np
import networkx as nx
from Source import pack, crack, find_num_seats, check_valid, first_partition_weighted, check_valid_weighted, pack_weighted

model_graph = nx.Graph()
model_graph.add_nodes_from([0, 1, 2, 3, 4])
model_graph.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (0, 1), (0, 2), (0, 3), (0, 4)])
attributes = {0: {'party' : 1, 'districted': False, 'pop': 100},
              1: {'party' : -1, 'districted': False, 'pop': 300},
              2: {'party' : -1, 'districted': False, 'pop' : 250},
              3: {'party' : -1, 'districted': False, 'pop': 200},
              4: {'party' : 1, 'districted': False, 'pop': 220}}
nx.set_node_attributes(model_graph, attributes)


model_graph_2 = nx.Graph()
attributes_dict = dict()
for i in range(17):
    model_graph_2.add_node(i)
    if (i < 12):
        attributes_dict[i] = {'party': -1, 'districted': False}
    else:
        attributes_dict[i] = {'party': 1, 'districted': False}

for i in range(4):
    model_graph_2.add_edge(i * 4 + 0, i * 4 + 1)
    model_graph_2.add_edge(i * 4 + 1, i * 4 + 2)
    model_graph_2.add_edge(i * 4 + 2, i * 4 + 3)
    model_graph_2.add_edge(i * 4 + 3, i * 4 + 0)

model_graph_2.add_edge(0, 4)
model_graph_2.add_edge(8, 4)
model_graph_2.add_edge(8, 12)
model_graph_2.add_edge(12, 0)


model_graph_2.add_edge(16, 0)
model_graph_2.add_edge(16, 4)
model_graph_2.add_edge(16, 8)
model_graph_2.add_edge(16, 12)
nx.set_node_attributes(model_graph_2, attributes_dict)

partition = first_partition_weighted(model_graph, k = 2)
print(partition)

# Works if delta = 300
print(check_valid_weighted(model_graph, partition, delta = 300))

# Does not work if delta =  200
print(check_valid_weighted(model_graph, partition, delta = 200))

# Check packing (small example)
partition_2 = pack_weighted(model_graph, k = 2)
print(partition_2)
print(check_valid_weighted(model_graph, partition_2, delta = 300))
