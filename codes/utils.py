"""
ユーティリティ関数
"""

import numpy as np


def is_diagonal(matrix, tol=1e-10):
    """
    3x3行列が対角行列かどうかを判定する

    Parameters
    ----------
    matrix : array_like
        判定する3x3行列
    tol : float, optional
        非対角要素が0とみなす許容誤差（デフォルト: 1e-10）

    Returns
    -------
    bool
        対角行列の場合True、そうでない場合False

    Examples
    --------
    >>> import numpy as np
    >>> from codes.utils import is_diagonal
    >>> box = np.diag([10.0, 10.0, 10.0])
    >>> is_diagonal(box)
    True
    >>> box[0, 1] = 0.1
    >>> is_diagonal(box)
    False
    """
    matrix = np.asarray(matrix)

    # 3x3行列であることを確認
    if matrix.shape != (3, 3):
        raise ValueError(f"行列は3x3である必要があります。現在の形状: {matrix.shape}")

    # 非対角要素を取得
    # 対角要素以外の要素をチェック
    mask = ~np.eye(3, dtype=bool)
    off_diagonal = matrix[mask]

    # 非対角要素がすべて許容誤差以内で0かどうかを判定
    return np.allclose(off_diagonal, 0.0, atol=tol)
