import numpy as np
import math
from typing import Callable


def round_half(n:float):
    nabs = abs(n)
    lo, hi = round(nabs) - .5, round(nabs) + .5
    return math.copysign(hi if abs(hi-nabs) < .5 else lo, n)


def find_closest_integral_point(p:np.ndarray):
    return np.array([round(x) for x in p])


def find_closest_half_point(p:np.ndarray):
    # print(round_half(3))
    # exit()
    return np.array([round_half(x) for x in p])


def iarray(a:np.array):
    return [int(e) for e in a]


def merge_predicate(
        predicate:Callable[[np.ndarray, np.ndarray], bool],
        a:np.ndarray, b:np.ndarray, axis:int
):
    """Merge two arrays according to `predicate` along `axis`."""
    i, j, imax, jmax = 0, 0, len(a), len(b)
    resultshape = [s for s in np.shape(a)]
    resultshape[axis] = imax + jmax
    merged = np.zeros(tuple(resultshape))
    while i < imax and j < jmax:
        ai, bj = a[i], b[j]
        if predicate(ai, bj):
            merged[i + j] = ai
            i += 1
        else:
            merged[i + j] = bj
            j += 1
    if i < imax:
        merged[i+j:] = a[i:]
    elif j < jmax:
        merged[i+j:] = b[j:]
    return merged
