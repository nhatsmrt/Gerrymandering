import numpy as np
import pandas as pd
import sklearn
import networkx as nx
from Source import first_partition, first_partition_splitline,\
    pack, crack, check_valid, beam_search_v2, GerrymanderGame, first_partition_v2,\
    find_corner, find_corner_closeness, find_corner_betweenness, find_corner_katz,\
    find_state_population,\
    first_partition_weighted,\
    pack_weighted_v2

from pathlib import Path

# Define the paths:
d = Path().resolve()
csv_path = str(d) + "/Data/data copy.csv"
df_data = pd.read_csv(csv_path)

# Lower case:
df_data['Municipality'] = df_data['Municipality'].apply(lambda x : x.lower())
df_data['Adjacent Municipalities'] = df_data['Adjacent Municipalities'].apply(lambda x : x.lower())

municipality_list = df_data['Municipality'].values
adjacency_lists = df_data['Adjacent Municipalities'].values
adjacency_lists_new = []
municipality_dict = dict()
index_to_name_dict = dict()
for i in range(len(municipality_list)):
    municipality_dict[municipality_list[i]] = i
    index_to_name_dict[i] = municipality_list[i]


for str in adjacency_lists:
    adjacency_list = str.split(", ")
    # print(adjacency_list)
    for i in range(len(adjacency_list)):
        adjacency_list[i] = municipality_dict[adjacency_list[i]]
    adjacency_lists_new.append(adjacency_list)

edge_list = []
for ind in range(len(adjacency_lists_new)):
    for i in adjacency_lists_new[ind]:
        edge_list.append((ind, i))

n_units = len(municipality_dict)
nodes = [i for i in range(n_units)]
mass_graph = nx.Graph()
mass_graph.add_nodes_from(nodes)
mass_graph.add_edges_from(edge_list)

# Adding attributes:
df_data['Vote Difference'] = df_data['Vote Difference'].map(lambda x: x.replace(',', ''))
party_dif = pd.to_numeric(df_data['Vote Difference']).values

df_data['Turnout'] = df_data['Turnout'].map(lambda x: x.replace(',', ''))
pop = pd.to_numeric(df_data['Turnout']).values


attributes_dict = dict()
for i in range(n_units):
    if party_dif[i] > 0:
        party = 1
    else:
        party = -1
    attributes_dict[i] = {'party': party, 'pop': pop[i], 'party_dif': party_dif[i]}

nx.set_node_attributes(mass_graph, attributes_dict)

corners_by_eye_str = ['salisbury', 'nantucket', 'mount washington', 'williamstown', 'dudley', 'quincy', 'barre', 'bridgewater', 'concord']
corners_bye_eye = [municipality_dict[str] for str in corners_by_eye_str]


# corners = find_corner(mass_graph)
# for corner in corners:
#     print(index_to_name_dict[corner])
# Test First Partition:
# partition = first_partition_v2(mass_graph, starting_list = corners_bye_eye)
# for part in partition
#     print(len(part))
#     print(part)
# print(check_valid(mass_graph, partition))

partition = first_partition_splitline(mass_graph, n_district = 9)
print(partition)
print(check_valid(mass_graph, partition))
# partition = pack_weighted_v2(mass_graph, n_district = 9, n_pack = 8)
# print(partition)
# print(index_to_name_dict[partition[-1][0]])




# print(first_partition(mass_graph, k = 9))