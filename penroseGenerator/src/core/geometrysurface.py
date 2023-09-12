""" Contains the GeometrySurface class. """
import abc

from numpy import ndarray

from penroseGenerator.src.core.transformsurface import TransformSurface


class GeometrySurface(TransformSurface):
    """ Allows drawing transformed primitives. """
    @abc.abstractmethod
    def draw_line_transformed(
        self, start: ndarray, end: ndarray, width: int=1, color:tuple[int,int,int,int]=(255, 255, 255, 255)
    ):
        """ Draw a line. """

    @abc.abstractmethod
    def draw_box_transformed(
        self, topleft: ndarray, size: ndarray, color:tuple[int,int,int,int]=(255, 0, 255, 255)
    ):
        """ Draw an empty rectangle. """

    @abc.abstractmethod
    def draw_dot_transformed(
        self, pos: ndarray, radius: float, color:tuple[int,int,int,int]=(0, 255, 255, 255)
    ):
        """ Draw a filled, non-antialiased circle. """
