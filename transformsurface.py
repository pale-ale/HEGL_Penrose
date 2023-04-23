import abc
from numpy import ndarray


class TransformSurface(abc.ABC):
    @abc.abstractmethod
    def transform_point_pixel(self, p:"ndarray") -> "ndarray":
        pass
