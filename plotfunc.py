from typing import Callable, Iterable
from geometrysurface import GeometrySurface
from numpy import ndarray


def plot_func(target:GeometrySurface, xvals:Iterable, func:Callable[[float], ndarray]):
    """ 
    Call `func` with each value inside `xvals` 
    and draw the resulting point onto `target`.
    """
    if len(xvals) < 2:
        return
    last = xvals[0]
    for val in xvals[1:]:
        target.draw_line_transformed(func(last), func(val))
        last = val
