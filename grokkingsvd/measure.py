import numpy as np
from typing import Tuple, List
import pyitlib.discrete_random_variable as drv

from grokkingsvd.utils import to_x_y


def measure_vars1(mat: np.array,
                  ) -> Tuple[List[float], List[str]]:

    """measure info theory variables"""

    xis, yis = to_x_y(mat)

    mi = drv.information_mutual_normalised(xis, yis, norm_factor='XY')
    xy = np.vstack((xis, yis))
    je = drv.entropy_joint(xy)
    xy = drv.entropy_conditional(xis, yis) / je
    yx = drv.entropy_conditional(yis, xis) / je

    props = [mi, xy, yx]
    names = ['I(X;Y)', 'H(X|Y)', 'H(Y|X)']

    return props, names


def measure_vars2(mat: np.array,
                  ) -> Tuple[List[float], List[str]]:
    s = np.linalg.svd(mat, compute_uv=False)
    assert np.max(s) == s[0]
    s1_norm = s[0] / np.sum(s)

    props = [s1_norm]
    names = ['s1/s']
    return props, names
