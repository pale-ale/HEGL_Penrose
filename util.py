import numpy as np
import math
from typing import Callable


def round_half(n:float):
    """ Return the closest number with fractional part 1/2. """
    nabs = abs(n)
    lo, hi = round(nabs) - .5, round(nabs) + .5
    return math.copysign(hi if abs(hi-nabs) < .5 else lo, n)


def find_closest_integral_point(p:np.ndarray):
    """ Return the closest point with integer value only. """
    return np.array([round(x) for x in p])


def find_closest_half_point(p:np.ndarray):
    """ Return the closest point with fractional parts of 1/2. """
    return np.array([round_half(x) for x in p])


def merge_sorted_predicate(
        predicate:Callable[[np.ndarray, np.ndarray], bool],
        a:np.ndarray, b:np.ndarray
):
    """Merge two sorted arrays according to `predicate` along `axis`."""
    if len(a) > 0 and not predicate(a[0], a[-1]):
        a = np.flip(a)
    if len(b) > 0 and not predicate(b[0], b[-1]):
        b = np.flip(b)
    i, j, imax, jmax = 0, 0, len(a), len(b)
    merged = np.zeros(imax + jmax)
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
    assert len(merged) == len(a) + len(b)
    return merged
