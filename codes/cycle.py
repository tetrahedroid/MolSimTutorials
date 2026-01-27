#!/usr/bin/env python

import networkx as nx

G = nx.Graph()
G.add_edges_from(
    [(0, 1), (1, 2), (2, 3), (3, 4), (4, 1), (0, 5), (5, 7), (7, 8), (8, 4), (5, 8)]
)

max_ring_size = 6
# Count the number of 2,3,4,...,max_ring_size-membered rings.
all_rings = []
for node in G:
    for neighbor in G.neighbors(node):
        if node < neighbor:
            paths = nx.all_simple_paths(
                G, source=node, target=neighbor, cutoff=max_ring_size - 1
            )
            for path in paths:
                path.sort()
                all_rings.append(path)

# Remove overlap.
uniq_all_rings_0 = []
for path in all_rings:
    if not path in uniq_all_rings_0:
        uniq_all_rings_0.append(path)

# Remove paths of len(path) == 2 because they are not "rings" but edges.
uniq_all_rings_1 = []
for path in uniq_all_rings_0:
    length = len(path)
    if length > 2:
        uniq_all_rings_1.append(path)

# Romove rings that completely include other ring(s).
tobe_removed = []
for ring_i in uniq_all_rings_1:
    n_size_i = len(ring_i)
    set_i = set(ring_i)
    j = 0
    for ring_j in uniq_all_rings_1:
        n_size_j = len(ring_j)
        if n_size_i < n_size_j:
            set_j = set(ring_j)
            and_set = set_i & set_j
            num_overlap = len(list(and_set))
            if num_overlap == n_size_i:
                tobe_removed.append(j)
        j = j + 1
