import abc
from numpy import ndarray
from transformsurface import TransformSurface


class GeometrySurface(TransformSurface):
    @abc.abstractmethod
    def draw_line_transformed(self, start: ndarray, end: ndarray, color=(255, 255, 255, 255)):
        pass

    @abc.abstractmethod
    def draw_box_transformed(self, topleft: ndarray, size: ndarray, color=(255, 0, 255, 255)):
        pass

    @abc.abstractmethod
    def draw_dot_transformed(self, pos: ndarray, radius: float, color=(0, 255, 255, 255)):
        pass
