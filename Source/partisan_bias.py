import numpy as np

def efficiency_gap(districts):
    n_voters = np.sum(districts)
    n_seat_A = (districts[:, 0] > districts[:, 1]).astype(np.int64)
    return (2 * np.sum(districts[:, 0]) - np.sum(n_seat_A * np.sum(districts, axis = 1))) / n_voters - 0.5

def jimmy_efficiency_gap(districts):
    n_voters = np.sum(districts, axis = 1)
    n_seat_A = (districts[:, 0] > districts[:, 1]).astype(np.int64)
    n_districts = districts.shape[0]
    return (np.sum((2 * districts[:, 0] - n_seat_A * n_voters) / n_voters)) / n_districts - 0.5


def jimmy_efficiency_gap_v2(districts):
    n_voters = np.sum(districts, axis = 1)
    total_voters = np.sum(districts)
    n_seat_A = (districts[:, 0] > districts[:, 1]).astype(np.int64)
    n_districts = districts.shape[0]
    return n_districts * np.sum((2 * districts[:, 0] - n_voters * 0.5 - n_seat_A * n_voters) * n_voters) / (total_voters * total_voters)

def daniel_efficiency_gap(districts):
    n_districts = districts.shape[0]
    n_seat_A = (districts[:, 0] > districts[:, 1]).astype(np.int64)
    return (2 * np.sum(districts[:, 0]) - np.sum(n_seat_A * np.sum(districts, axis = 1))) / n_districts - 0.5




districts = np.array([[95, 5], [40, 60], [75, 25], [45, 55], [45, 55]])
print(daniel_efficiency_gap(districts))
