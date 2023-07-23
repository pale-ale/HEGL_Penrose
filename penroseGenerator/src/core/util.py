""" Contains some simple helper methods. """

import math
from typing import Callable

import numpy as np

def round_half(number:float):
    """ Return the closest number with fractional part 1/2. """
    nabs = abs(number)
    lo_int, hi_int = round(nabs) - .5, round(nabs) + .5
    return math.copysign(hi_int if abs(hi_int-nabs) < .5 else lo_int, number)


def find_closest_integral_point(point:np.ndarray):
    """ Return the closest point with integer value only. """
    return np.array([round(x) for x in point])


def find_closest_half_point(point:np.ndarray):
    """ Return the closest point with fractional parts of 1/2. """
    return np.array([round_half(x) for x in point])


def merge_sorted_predicate(
        predicate:Callable[[np.ndarray, np.ndarray], bool],
        array1:np.ndarray, array2:np.ndarray
):
    """Merge two sorted arrays according to `predicate` along `axis`."""
    if len(array1) > 0 and not predicate(array1[0], array1[-1]):
        array1 = np.flip(array1)
    if len(array2) > 0 and not predicate(array2[0], array2[-1]):
        array2 = np.flip(array2)
    i, j, imax, jmax = 0, 0, len(array1), len(array2)
    merged = np.zeros(imax + jmax)
    while i < imax and j < jmax:
        ai, bj = array1[i], array2[j]
        if predicate(ai, bj):
            merged[i + j] = ai
            i += 1
        else:
            merged[i + j] = bj
            j += 1
    if i < imax:
        merged[i+j:] = array1[i:]
    elif j < jmax:
        merged[i+j:] = array2[j:]
    assert len(merged) == len(array1) + len(array2)
    return merged
