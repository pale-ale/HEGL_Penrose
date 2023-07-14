from src.core.geometry import Line2D, intersect_line2D
from unittest import TestCase
from numpy import pi, ndarray, ones, array

def close_to(a,b):
    if isinstance(a, ndarray) and isinstance(b, ndarray):
      return abs(a-b).all() < 1e-10
    return abs(a-b) < 1e-10

def test_lineinstersect_len1():
    l1 = Line2D(-1, 0)
    l2 = Line2D(1, pi/2)
    intersection = intersect_line2D(l1, l2)
    assert intersection is not None
    assert close_to(intersection, ones(2))

def test_lineinstersect():
    l1 = Line2D(-1, 0)
    l1.direction = array([2,0])
    l2 = Line2D(1, pi/2)
    intersection = intersect_line2D(l1, l2)
    assert intersection is not None
    assert close_to(intersection, ones(2))