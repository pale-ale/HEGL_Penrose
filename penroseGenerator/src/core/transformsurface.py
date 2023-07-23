""" Contains the TransformSurface class. """

import abc
from numpy import ndarray


class TransformSurface(abc.ABC):
    """ Can transform points into screen space. """
    @abc.abstractmethod
    def transform_point_pixel(self, point:"ndarray") -> "ndarray":
        """ Transform a point into screen space. """
