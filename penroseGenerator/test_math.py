""" Some simple sanity checks for basic algebra stuff. """

from numpy import pi, ndarray, ones, array

from penroseGenerator.src.core.geometry import Line2D, intersect_line2d

def close_to(val1,val2):
    """ Are val1 and val2 close enough to be ocnsidered equal? """
    if isinstance(val1, ndarray) and isinstance(val2, ndarray):
        return abs(val1-val2).all() < 1e-10
    return abs(val1-val2) < 1e-10

def test_lineinstersect_len1():
    """ Unsures the intersection is calculated correctly with length == 1. """
    line1 = Line2D(-1, 0)
    line2 = Line2D(1, pi/2)
    intersection = intersect_line2d(line1, line2)
    assert intersection is not None
    assert close_to(intersection, ones(2))

def test_lineinstersect():
    """ Unsures the intersection is calculated correctly with length != 1. """
    line1 = Line2D(-1, 0)
    line1.direction = array([2,0])
    line2 = Line2D(1, pi/2)
    intersection = intersect_line2d(line1, line2)
    assert intersection is not None
    assert close_to(intersection, ones(2))
