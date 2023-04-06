from typing import Callable


def plot_func(target, xvals, func:Callable[[float],float]):
    if len(xvals) < 2:
        return
    last = xvals[0]
    for val in xvals[1:]:
        target.draw_line_transformed((last, func(last)), (val, func(val)))
        last = val
