import numpy as np
import pandas as pd
import sklearn

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


from pathlib import Path

# Define the paths:
d = Path().resolve()
data_2014_path = str(d) + "/Data/2014-us"

df_lower = pd.read_csv(data_2014_path + "/state_lower.csv")

measures = ["Polsby-Popper", "Schwartzberg", "Area/Convex Hull", "Reock"]
X = df_lower[measures].values

kmeans = KMeans(init='random', n_clusters= 2, n_init=10).fit(X)
labels = kmeans.labels_

colors = []
for label in labels:
    if label == 0:
        colors.append("red")
    else:
        colors.append("blue")
print("Finish creating colors")



pca = PCA(n_components = 2)
X_reduced = pca.fit_transform(X)

plt.scatter(x = X_reduced[:, 0], y = X_reduced[:, 1], c = colors)

# pca = PCA(n_components = 3)
# X_reduced = pca.fit_transform(X)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(xs = X_reduced[:, 0], ys = X_reduced[:, 1], zs = X_reduced[:, 2], c = colors)

plt.show()

