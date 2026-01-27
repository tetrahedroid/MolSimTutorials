#!/usr/bin/env python

import sys

title = sys.stdin.readline()
n_atom = int(sys.stdin.readline())
for i in range(n_atom):
    line = sys.stdin.readline()
    residue_id = int(line[0:5])
    residue = line[5:10].strip()
    atom = line[10:15].strip()
    atom_id = int(line[15:20])
    x = float(line[20:28])
    y = float(line[28:36])
    z = float(line[36:44])
    # 速度は省略
    print(f"{atom_id} {x} {y} {z}")

cell = [float(x) for x in sys.stdin.readline().split()]
print(cell)
# strip()関数は，文字列の先頭と末尾の空白をとりのぞく．
