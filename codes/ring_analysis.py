#!/usr/bin/env python
# groファイルを読みこみ、HBをつないでリングの統計をとる。
# この部分はMolSimTutorialsからそのままもってきた

from codes.read_gro3 import read_gro

import networkx as nx

# 松本作: 周期境界条件のもとで近接点対をリストする
import pairlist as pl

# 松本作: グラフの中にサイクルをさがす
from cycless import cycles

for frame in read_gro(sys.stdin):
    # シミュレーションセル
    cell = frame["cell"]

    # シミュレーションセルの逆行列
    celli = np.linalg.inv(cell)

    # 酸素原子の座標
    oxygens = frame["position"][frame["atom"] == "OW", :]
    # 水素原子1の座標
    hydrogens1 = frame["position"][frame["atom"] == "HW1", :]
    # 水素原子2の座標
    hydrogens2 = frame["position"][frame["atom"] == "HW1", :]
    # 酸素原子の座標をセルの逆行列をかけてfractional coordinateに変換
    rO = oxygens @ celli
    # 水素原子1の座標をセルの逆行列をかけてfractional coordinateに変換
    rH1 = hydrogens1 @ celli
    # 水素原子2の座標をセルの逆行列をかけてfractional coordinateに変換
    rH2 = hydrogens2 @ celli

    # グラフを作成
    g = nx.Graph()
    # 酸素原子と水素原子1の距離が0.245以下の場合
    for o, h1, d in pl.pairs_iter(rO, 0.245, cell, pos2=rH1):
        # 距離が0.1以下の場合は、グラフに追加しない(共有結合)
        if d > 0.1:
            g.add_edge(o, h1)
    for o, h2, d in pl.pairs_iter(rO, 0.245, cell, pos2=rH2):
        if d > 0.1:
            g.add_edge(o, h2)
    for cycle in cycles.cycles_iter(g, 10):
        # 環のサイズが10以下の場合は、環のサイズを出力
        print(len(cycle))
