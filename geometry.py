import math
from ctypes import c_float
from numpy import ndarray

import numpy as np
import scipy.linalg
import sdl2
import sdl2.ext
from geometrysurface import GeometrySurface
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mathpentagrid import Lattice

class Line2D:
    """
    This class represents a two dimensional line.
    It has an angle, and a distance from (0,0), always offset perpendicular to the slope.
    """

    def __init__(self, dist_to_zero: float, angle: float) -> None:
        self.dist_to_zero = dist_to_zero
        self._angle = angle
        self._direction = np.array([math.cos(angle), math.sin(angle)])
    
    @classmethod
    def copyconstruct(cls, line:"Line2D"):
        return cls(line.dist_to_zero, line.angle)

    @property
    def angle(self):
        """ The angle of the line in radians. """
        return self._angle
    
    @property
    def start(self):
        return self.normal * self.dist_to_zero

    @property
    def normal(self):
        return np.flip(self.direction) * (1,-1)

    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, direction:np.ndarray):
        self._direction = direction
        self._angle = np.arctan2(*direction)
    
    @angle.setter
    def angle(self, value):
        self._angle = value
        self.direction = np.array([math.cos(value), math.sin(value)])

    def __call__(self, t: float):
        """ Evaluate the line with parameter value `t` and return the 2D point. """
        return self.start + t * self.direction

    def get_param(self, dim: int, val: float) -> float:
        """ Return a parameter whose point has value `x` in dimension `n`. """
        return (val - self.normal[dim] * self.dist_to_zero) / (self.direction[dim])

    def get_bounding_params(self, lo, hi, minparam, maxparam):
        """
        Return the two parameters that have points on the edge of the rect,
        or None if the bounding box doesnt intersect.
        """
        rect = sdl2.SDL_FRect(*lo, *(hi-lo)+1)
        maxextent = scipy.linalg.norm(hi-lo) * 2
        assert maxextent > 0
        c_x1, c_y1, c_x2, c_y2 = [
            c_float(x) for x in [*self(minparam), *self(maxparam)]]
        intersects = sdl2.SDL_IntersectFRectAndLine(
            rect, c_x1, c_y1, c_x2, c_y2)
        i1, i2 = None, None
        if intersects and (c_x1 != c_x2 or c_y1 != c_y2):
            if abs(self.direction[0]) > abs(self.direction[1]):
                i1, i2 = self.get_param(0, c_x1.value), self.get_param(0, c_x2.value)
            else:
                i1, i2 = self.get_param(1, c_y1.value), self.get_param(1, c_y2.value)
        return i1, i2

    def get_int_values(self, dim: int, lo: ndarray, hi: ndarray):
        """
        Return every parameter whose point has an integral value for dimension `n`
        and lies between `lo` and `hi` component-wise inclusive.
        """
        assert np.all(lo < hi)
        outer_lo_int = np.ceil(lo).astype(np.int16)
        outer_hi_int = np.floor(hi).astype(np.int16)
        assert np.all(outer_lo_int < outer_hi_int)
        p1, p2 = self.get_bounding_params(outer_lo_int, outer_hi_int, -10, 10)
        if not p1 or not p2:
            return np.array(0)
        bounds = np.array([self(p1), self(p2)])
        lo_int = np.floor(np.min(bounds, axis=0)).astype(np.int16)
        hi_int = np.ceil(np.max(bounds, axis=0)).astype(np.int16)
        integral_values = []
        for val in range(lo_int[dim], hi_int[dim] + 1):
            param = self.get_param(dim, val)
            if np.all(lo_int <= self(param)) and np.all(self(param) <= hi_int):
                integral_values.append(param)
        return np.array(integral_values)
    
    def is_parallel(self, line:"Line2D"):
        return abs(self.angle - line.angle) <= 1e-10
    
    def __eq__(self, __value: "Line2D") -> bool:
        return self.is_parallel(__value) and \
            abs(self.dist_to_zero - __value.dist_to_zero) <= 1e-10

    def draw(self, target: GeometrySurface, bottomleft, topright, color=(100,100,100,255)):
        p1, p2 = self.get_bounding_params(bottomleft, topright, -1000, 1000)
        if p1 and p2:
            target.draw_line_transformed(self(p1), self(p2), color=color)
    
    @staticmethod
    def draw_lattice(target: GeometrySurface, bottomleft, topright, lattice:"Lattice", color=(100,100,100,255)):
        line, start, stop, step, offset = lattice
        linecpy = Line2D(line.dist_to_zero, line.angle)
        for i in range(start, stop+1):
            linecpy.dist_to_zero = i * step + offset
            linecpy.draw(target, bottomleft, topright, color)

def intersect_line2D(l1:Line2D, l2:Line2D):
    l1sx, l1sy = l1.start
    l1dx, l1dy = l1.direction
    l2sx, l2sy = l2.start
    l2dx, l2dy = l2.direction
    if l1dx == 0 and l2dx == 0 or l1dy == 0 and l2dy == 0:
        return None
    if all(l1.direction == l2.direction):
        return None
    return l1((l2dx * (l1sy - l2sy) + l2dy * (l2sx - l1sx)) / (l1dx * l2dy - l1dy * l2dx))
