""" Contains some geometry-related classes and helper functions. """
import math
from ctypes import c_float

import numpy as np
import sdl2
import sdl2.ext

from penroseGenerator.src.core.geometrysurface import GeometrySurface

Lattice = tuple["Line2D", int, int, float, float]
""" 
Represents a group of evenly spaced, parallel lines, translated orthogonally by the last float. 
"""


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
        """ Create a new, independent line. """
        return cls(line.dist_to_zero, line.angle)

    @property
    def angle(self):
        """ The angle of the line in radians. """
        return self._angle

    @property
    def start(self):
        """ The \"starting point\" of this line. """
        return self.normal * self.dist_to_zero

    @property
    def normal(self):
        """ Returns a normalized orthogonal vector. """
        orth = np.flip(self.direction) * (1,-1)
        return orth / np.linalg.norm(orth)

    @property
    def direction(self):
        """ The direction as a 2D-vector. """
        return self._direction

    @direction.setter
    def direction(self, direction:np.ndarray):
        self._direction = direction
        self._angle = np.arctan2(*direction)

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.direction = np.array([math.sin(value), math.cos(value)])

    def __call__(self, param: float):
        """ Evaluate the line with parameter value `param` and return the 2D point. """
        return self.start + param * self.direction

    def get_param(self, dim: int, val: float) -> float:
        """ Return a parameter whose point has value `x` in dimension `n`. """
        return (val - self.normal[dim] * self.dist_to_zero) / (self.direction[dim])

    def get_bounding_params(self, lower, higher, minparam, maxparam):
        """
        Return the two parameters that have points on the edge of the rect,
        or None if the bounding box doesnt intersect.
        """
        rect = sdl2.SDL_FRect(*lower, *(higher-lower)+1)
        maxextent = np.linalg.norm(higher-lower) * 2
        assert maxextent > 0
        c_x1, c_y1, c_x2, c_y2 = [
            c_float(x) for x in [*self(minparam), *self(maxparam)]]
        intersects = sdl2.SDL_IntersectFRectAndLine(
            rect, c_x1, c_y1, c_x2, c_y2)
        int1, int2 = None, None
        if intersects and (c_x1 != c_x2 or c_y1 != c_y2):
            if abs(self.direction[0]) > abs(self.direction[1]):
                int1, int2 = self.get_param(0, c_x1.value), self.get_param(0, c_x2.value)
            else:
                int1, int2 = self.get_param(1, c_y1.value), self.get_param(1, c_y2.value)
        return int1, int2

    def get_int_values(self, dim: int, lower: np.ndarray, higher: np.ndarray):
        """
        Return every parameter whose point has an integral value for dimension `n`
        and lies between `lo` and `hi` component-wise inclusive.
        """
        assert np.all(lower < higher)
        outer_lo_int = np.ceil(lower).astype(np.int16)
        outer_hi_int = np.floor(higher).astype(np.int16)
        assert np.all(outer_lo_int < outer_hi_int)
        param1, param2 = self.get_bounding_params(outer_lo_int, outer_hi_int, -10, 10)
        if not param1 or not param2:
            return np.array(0)
        bounds = np.array([self(param1), self(param2)])
        lo_int = np.floor(np.min(bounds, axis=0)).astype(np.int16)
        hi_int = np.ceil(np.max(bounds, axis=0)).astype(np.int16)
        integral_values = []
        for val in range(lo_int[dim], hi_int[dim] + 1):
            param = self.get_param(dim, val)
            if np.all(lo_int <= self(param)) and np.all(self(param) <= hi_int):
                integral_values.append(param)
        return np.array(integral_values)

    def is_parallel(self, line:"Line2D"):
        """ Check if a line is parallel to  this one. """
        return abs(self.angle - line.angle) <= 1e-10

    def __eq__(self, __value: "Line2D") -> bool:
        return self.is_parallel(__value) and \
            abs(self.dist_to_zero - __value.dist_to_zero) <= 1e-10

    def draw(self, target: GeometrySurface, bottomleft, topright, color=(100,100,100,255)):
        """ Draw the line to a target. """
        param1, param2 = self.get_bounding_params(bottomleft, topright, -1000, 1000)
        if param1 and param2:
            target.draw_line_transformed(self(param1), self(param2), color=color)
            target.draw_dot_transformed(self(param2), 3, color=color)

    @staticmethod
    def draw_lattice(
        target: GeometrySurface,
        bottomleft,
        topright,
        lattice:"Lattice",
        color=(100,100,100,255)
    ):
        """ Draw the lattice. """
        line, start, stop, step, offset = lattice
        linecpy = Line2D(line.dist_to_zero, line.angle)
        for i in range(start, stop+1):
            linecpy.dist_to_zero = i * step + offset
            linecpy.draw(target, bottomleft, topright, color)

    def __repr__(self) -> str:
        return f"Line2D: Direction={self.direction}, Dist_to_zero={self.dist_to_zero}"

def intersect_line2d(line1:Line2D, line2:Line2D):
    """ Return the intersection point between `line1` and `line2` or None for edge cases. """
    l1sx, l1sy = line1.start
    l1dx, l1dy = line1.direction
    l2sx, l2sy = line2.start
    l2dx, l2dy = line2.direction
    if l1dx == 0 and l2dx == 0 or l1dy == 0 and l2dy == 0:
        return None
    if all(line1.direction == line2.direction):
        return None
    return line1((l2dx * (l1sy - l2sy) + l2dy * (l2sx - l1sx)) / (l1dx * l2dy - l1dy * l2dx))

def project_point_line_2d(point: np.ndarray, start: np.ndarray, direction: np.ndarray):
    """ 
    Project the point `point` onto the line starting at `start` 
    with direction `dir` orthogonally.
    """
    assert (norm_d := np.linalg.norm(direction)) != 0
    pointx, pointy = point
    startx, starty = start
    direction = direction /norm_d
    dirx, diry = direction
    best_param = (dirx * (pointx - startx) + diry * (pointy - starty)) / (dirx**2 + diry**2)
    return start + best_param * direction
