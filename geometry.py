import math
from ctypes import c_float
from numpy import ndarray

import numpy as np
import scipy.linalg
import sdl2
import sdl2.ext
from geometrysurface import GeometrySurface

class Line2D:
    """
    This class represents a two dimensional line.
    It has an angle, and a distance from (0,0), always offset perpendicular to the slope.
    """

    def __init__(self, dist_to_zero: float, angle: float) -> None:
        self.dist_to_zero = dist_to_zero
        self.angle = angle
        self.direction = np.array([math.cos(angle), math.sin(angle)])
        self.normal = np.flip(self.direction)

    @property
    def angle(self):
        """ The angle of the line in radians. """
        return self._angle
    
    @property
    def start(self):
        return self.normal * self.dist_to_zero

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.direction = np.array([math.cos(value), math.sin(value)])
        self.normal = np.flip(self.direction) * (1,-1)

    def __call__(self, t: float):
        """ Evaluate the line with parameter value `t` and return the 2D point. """
        return self.normal * self.dist_to_zero + t * self.direction

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
                i1, i2 = self.get_param(0, c_x1), self.get_param(0, c_x2)
            else:
                i1, i2 = self.get_param(1, c_y1), self.get_param(1, c_y2)
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
        if not p1:
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

    def draw(self, target: GeometrySurface, bottomleft, topright):
        p1, p2 = self.get_bounding_params(bottomleft, topright, -1000, 1000)
        if p1:
            target.draw_line_transformed(self(p1), self(p2))
            target.draw_line_transformed(np.array([0,0]), self(0), (100,100,100,255))
