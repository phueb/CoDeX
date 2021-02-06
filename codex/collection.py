import numpy as np
from typing import Tuple, Callable


def transform_0(co_mat: np.array,
                step: int,
                ) -> np.array:
    res = co_mat.copy()

    res[5, 5] -= step
    res[5, 0] += step

    res[4, 4] -= step
    res[4, 0] += step

    assert res.sum() == co_mat.sum()

    return res


def transform_1(co_mat: np.array,
                step: int,
                ) -> np.array:
    res = co_mat.copy()

    res[0, 8] -= step
    res[1, 8] -= step
    res[2, 8] -= step
    res[3, 7] -= step
    res[4, 7] -= step
    res[5, 7] -= step

    res[:, 6] += step

    assert res.sum() == co_mat.sum()

    return res


def get_width_height_pixels(collection_id: int,
                            ) -> Tuple[int, int]:
    if collection_id == 0:
        return 300, 300
    elif collection_id == 1:
        return 400, 300
    else:
        raise ValueError(f'Did not find collection for id={collection_id}')


def load_collection(collection_id: int,
                    ) -> Tuple[np.array, Callable[[np.array, int], np.array]]:

    if collection_id == 0:
        __ = 0
        _1 = 10
        _2 = 10
        _3 = 10
        co_mat_original = np.array([
            [_2, __, __, __, __, __],
            [__, _2, __, __, __, __],
            [__, __, _2, __, __, __],
            [__, __, __, _2, __, __],
            [__, __, __, __, _2, __],
            [__, __, __, __, __, _2],
        ])
        return co_mat_original, transform_0
    elif collection_id == 1:
        __ = 0
        _1 = 10
        _2 = 10
        _3 = 10
        co_mat_original = np.array([
            [_1, __, __, __, __, __, _3, __, _2],
            [__, _1, __, __, __, __, _3, __, _2],
            [__, __, _1, __, __, __, _3, __, _2],
            [__, __, __, _1, __, __, _3, _2, __],
            [__, __, __, __, _1, __, _3, _2, __],
            [__, __, __, __, __, _1, _3, _2, __],
        ])
        return co_mat_original, transform_1
    else:
        raise ValueError(f'Did not find collection for id={collection_id}')
