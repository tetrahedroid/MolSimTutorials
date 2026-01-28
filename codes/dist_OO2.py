#!/usr/bin/env python
import sys
import numpy as np
from read_gro3 import read_gro

for frame in read_gro(sys.stdin):
    cell = frame["cell"]
    positions = frame["position"]
    atoms = frame["atom"]
    oxygens = positions[atoms == "OW"]
    celli = np.linalg.inv(cell)
    d = (oxygens - oxygens[0]) @ celli
    d -= np.floor(d + 0.5)
    L = np.linalg.norm(d @ cell, axis=1)
    for r in L:
        print(r)
