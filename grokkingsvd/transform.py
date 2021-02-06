import numpy as np


def move_diag_to_col(co_mat: np.array,
                     step: int,
                     ) -> np.array:
    # transform
    res = co_mat.copy()
    res[5, 5] -= step
    res[5, 0] += step

    res[4, 4] -= step
    res[4, 0] += step

    assert res.sum() == co_mat.sum()

    return res