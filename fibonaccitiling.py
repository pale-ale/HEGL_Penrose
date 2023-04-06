import math

import numpy as np
import sdl2
import sdl2.ext

from plotfunc import plot_func
from squaregrid import Squaregrid
from util import find_closest_half_point, merge_predicate
from windowmanager import WindowManager
from projection import project_point_line_2d

WINDOWSIZE = (800, 800)
WINDOWCENTER = (WINDOWSIZE[0]/2, WINDOWSIZE[1]/2)
GRID_SUBDIVISIONS = (16,16)

sdl2.ext.init()

wm = WindowManager("Fibonacchitiling", WINDOWSIZE)

grid = Squaregrid(WINDOWSIZE, *GRID_SUBDIVISIONS)
grid.origin = WINDOWCENTER
grid.xyscale = np.array((50, -50))

PHI = (1+math.sqrt(5)) / 2
incline = -1/PHI
inclinescale = 1.0


def get_f(incline:float):
    return lambda x: incline*x


def get_inv_f(incline:float):
    return lambda x: 1/incline*x


def is_integral(a:float):
    return a - int(a) == 0


def get_lattice_pts(startxy, endxy, func, invfunc):
    startx, starty = startxy
    endx, endy = endxy
    xvals = np.fromiter(range(startx, endx+1), int)
    yvals = np.fromiter(range(min(starty, endy), max(starty, endy)+1), int)
    x_pts = np.array([xvals, np.apply_along_axis(func, 0, xvals)]).transpose()
    y_pts = np.array([np.apply_along_axis(invfunc, 0, yvals), yvals]).transpose()
    pts = merge_predicate(lambda p1,p2: p1[0] < p2[0], x_pts, y_pts, 0)
    lpts = np.zeros((len(pts)-1,2))
    for i in range(len(pts)-1):
        halfway = (pts[i+1] + pts[i])/2
        lpts[i] = find_closest_half_point(halfway)
    return lpts


def draw_pt_proj_between(target:Squaregrid, p:np.ndarray, a:np.ndarray, b:np.ndarray):
    """Draw a line between `p` and the orthognal from `a` to `b`."""
    pp = project_point_line_2d(p, a, b-a)
    target.draw_line_transformed(p, pp)


def tickmethod():
    global incline
    incline += inclinescale * 0.005
    sdl2.SDL_SetRenderDrawColor(grid.renderer,0,0,0,0)
    sdl2.SDL_RenderClear(grid.renderer)
    f, inv_f = get_f(incline), get_inv_f(incline)
    xmin, xmax = -4, 4
    lpts = get_lattice_pts((xmin,int(f(xmin))), (xmax,int(f(xmax))), f, inv_f)
    for lpt in lpts:
        grid.draw_dot_transformed(lpt, 6)
    plot_func(grid, np.linspace(xmin,xmax,2), f)
    for lpt in lpts:
        draw_pt_proj_between(grid, lpt, np.array([xmin,f(xmin)]), np.array([xmax, f(xmax)]))
    grid.draw(wm.renderer)
    sdl2.SDL_RenderPresent(grid.renderer)


def reverse(event):
    global inclinescale
    if event.type == sdl2.SDL_KEYDOWN:
        inclinescale = -1.0
        return
    inclinescale = 1.0


wm.tickmethod = tickmethod
wm.set_key_event(sdl2.keycode.SDLK_LALT, reverse)
wm.run()
