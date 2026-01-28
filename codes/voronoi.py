import sys
import numpy as np
import pyvoro
from codes.read_gro3 import read_gro
from codes.utils import is_diagonal


for frame in read_gro(sys.stdin):
    # シミュレーションセル（対角行列を仮定）
    box = frame["cell"]
    assert is_diagonal(box), "シミュレーションセルは直方体である必要があります"

    # 酸素原子の座標
    oxygens = frame["position"][frame["atom"] == "OW", :]

    # 直方体セルのサイズ
    Lx, Ly, Lz = box[0, 0], box[1, 1], box[2, 2]

    # pyvoro による周期 Voronoi 解析
    # limits: 各次元の最小値と最大値
    # dispersion: ブロックサイズ（隣接する可能性のある点間の最大距離）
    # periodic: 各次元の周期性
    cells = pyvoro.compute_voronoi(
        oxygens.tolist(),
        limits=[[0, Lx], [0, Ly], [0, Lz]],
        dispersion=max(Lx, Ly, Lz) / 3.0,  # 適切なブロックサイズ
        periodic=[True, True, True],
    )

    # 各 Voronoi セルの面数と体積を出力
    for i, cell in enumerate(cells):
        nfaces = len(cell["faces"])
        volume = cell["volume"]
        print(f"Cell {i} has {nfaces} faces and a volume of {volume}")
