from typing import List, Dict, Union
import numpy as np


def to_x_y(mat):
    xis = []
    yis = []
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            xis += [i] * v
            yis += [j] * v
    return xis, yis


def to_columnar(matrices: List[np.array],
                ) -> Dict[str, List[Union[float, int]]]:
    """
    convert multiple matrices into a dict,
    where each entry corresponds to a single matrix element:
    - the index of the matrix the element is a part of,
    - the row index
    - the col index
    - the element's value

      """
    res = {'x': [],
           'y': [],
           'z': [],
           's': [],  # step, or which matrix in list of matrices
           }

    for step, m in enumerate(matrices):
        for yi in range(m.shape[0]):
            for xi in range(m.shape[1]):

                res['y'].append(yi)
                res['x'].append(xi)
                res['z'].append(m[yi, xi])
                res['s'].append(step)

    return res
