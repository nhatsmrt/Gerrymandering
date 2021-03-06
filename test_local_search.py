import numpy as np
import networkx as nx
from Source import GerrymanderGame_v2, DQN, beam_search, beam_search_v2


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

env = GerrymanderGame_v2(G = model_graph_2, n_districts = 4, n_units = 17)


best_result = beam_search(env = env, initial_partition = env.first_partition())
best_result2 = beam_search_v2(env = env, initial_partition = env.first_partition())

print(best_result2)