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

corners_by_eye_str = ['salisbury', 'nantucket', 'mount washington', 'williamstown', 'dudley', 'quincy', 'barre', 'bridgewater', 'concord']
corners_bye_eye = [municipality_dict[str] for str in corners_by_eye_str]

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

# env = GerrymanderGame(mass_graph, n_districts = 9, n_units = n_units)
# initial_partition = first_partition_v2(mass_graph, starting_list = corners_bye_eye)
# final_partition = beam_search_v2(env = env, initial_partition = initial_partition, search_depth = 100, n_keep = 5)

partition = [[6, 8, 30, 38, 71, 79, 92, 104, 106, 115, 118, 127, 143, 148, 162, 163, 164, 165, 167, 179, 180, 183, 195, 204, 205, 209, 212, 228, 245, 251, 253, 257, 258, 283, 290, 294, 297, 304, 319, 323, 341], [2, 9, 20, 36, 41, 55, 62, 72, 75, 86, 89, 94, 95, 96, 108, 125, 144, 171, 196, 200, 220, 223, 230, 238, 241, 246, 260, 264, 272, 291, 295, 299, 317, 326, 333, 350], [4, 5, 22, 33, 59, 61, 87, 90, 111, 112, 116, 126, 131, 136, 142, 149, 151, 158, 182, 192, 193, 194, 202, 213, 224, 255, 259, 266, 274, 275, 278, 280, 282, 296, 301, 312, 324, 325, 328, 330, 348], [3, 13, 47, 53, 58, 60, 63, 66, 68, 69, 70, 74, 98, 105, 107, 113, 120, 128, 129, 147, 155, 189, 199, 208, 232, 235, 236, 248, 252, 262, 267, 288, 336, 339, 340, 344], [17, 28, 32, 39, 43, 45, 54, 64, 77, 80, 84, 85, 109, 119, 134, 137, 138, 150, 178, 185, 187, 190, 211, 214, 215, 225, 227, 270, 277, 279, 286, 289, 303, 305, 310, 315, 320, 327, 338, 347], [0, 18, 35, 40, 46, 49, 50, 57, 65, 73, 78, 93, 130, 132, 135, 141, 174, 175, 177, 186, 188, 198, 206, 219, 242, 243, 247, 261, 263, 273, 284, 313, 334, 335, 345], [7, 11, 12, 15, 21, 24, 29, 91, 97, 103, 110, 123, 133, 139, 152, 153, 160, 161, 191, 201, 203, 216, 221, 222, 226, 229, 233, 234, 240, 254, 256, 271, 281, 293, 298, 308, 311, 318, 322, 331, 342], [16, 25, 27, 42, 44, 52, 76, 82, 83, 88, 99, 101, 102, 117, 121, 122, 145, 166, 168, 170, 172, 176, 181, 184, 207, 210, 217, 218, 237, 239, 244, 249, 250, 265, 292, 302, 306, 309, 321, 337, 349], [1, 10, 14, 19, 23, 26, 31, 34, 37, 48, 51, 56, 67, 81, 100, 114, 124, 140, 146, 154, 156, 157, 159, 169, 173, 197, 231, 268, 269, 276, 285, 287, 300, 307, 314, 316, 329, 332, 343, 346]]
print(check_valid(mass_graph, partition))

# print(final_partition)
# print(env.find_num_seats(partition = final_partition))