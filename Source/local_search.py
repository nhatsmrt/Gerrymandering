import numpy as np

def beam_search(env, initial_partition, search_depth = 2, n_keep = 5):
    initial_seat = env.find_num_seats(initial_partition)
    list_all = [(initial_partition, initial_seat)]
    keep_list = [(initial_partition, initial_seat)]

    for depth in range(search_depth):

        for partition, seat in keep_list:
            for position in range(env._n_units):
                for displacement in range(1, env._n_districts):
                    action = (position, displacement)
                    state = env.partition_to_state(partition)
                    new_state = env.act(state, action)
                    new_partition = env.state_to_partition(new_state)
                    n_seats = env.find_num_seats(new_partition)
                    list_all.append((new_partition, n_seats))

        keep_list =  sorted(list_all, key = lambda tuple: tuple[1])[:-n_keep]
        list_all = sorted(list_all, key = lambda tuple: tuple[1])[:-n_keep]


    return keep_list[-1]

def check_in(list, str):
    for s in list:
        if s == str:
            return True

    return False

def beam_search_v2(env, initial_partition, search_depth = 10, n_keep = 5):
    initial_seat = env.find_num_seats(initial_partition)
    list_all = np.array([[initial_partition, initial_seat]])
    keep_list = np.array([[initial_partition, initial_seat]])
    state_list = []
    state_list.append(str(env.partition_to_state(initial_partition)))

    for depth in range(search_depth):

        for partition, seat in keep_list:
            for position in range(env._n_units):
                for displacement in range(1, env._n_districts):
                    action = (position, displacement)
                    state = env.partition_to_state(partition)
                    new_state = env.act(state, action)
                    new_state_str = str(new_state)
                    if not check_in(state_list, new_state_str):
                        new_partition = env.state_to_partition(new_state)
                        n_seats = env.find_num_seats(new_partition)
                        list_all = np.append(list_all, [[new_partition, n_seats]], axis = 0)
                        state_list.append(new_state_str)
        ind = np.argsort(list_all[:, 1])[-n_keep:]
        keep_list =  list_all[ind, :]
        list_all = list_all[ind, :]
        print("Depth " + str(depth))
        # print(keep_list)

    return keep_list[np.argsort(keep_list[:, 1])[-1], :]
