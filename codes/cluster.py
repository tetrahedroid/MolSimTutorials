#!/usr/bin/env python

import networkx as nx

G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (3, 4), (4, 5), (5, 6), (6, 3), (7, 8)])
G.add_nodes_from([9, 10])

n_cluster_size_threshold = 2

# Generate connected components (i.e., clusters)
all_components = []
for component in nx.connected_components(G):
    tmp_nodes = []
    for node in component:
        tmp_nodes.append(int(node))
    tmp_nodes.sort()
    if len(tmp_nodes) > n_cluster_size_threshold:
        all_components.append(tmp_nodes)

# Sort so that larger component becomes earlier
all_components.sort(key=lambda x: len(x), reverse=True)

n_components = len(all_components)
print("number of clusters:", n_components)
print("cluster size: ", end="")
for component in all_components:
    print(len(component), end=" ")
print()
