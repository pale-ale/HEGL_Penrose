import math

import numpy as np
import sdl2
import sdl2.ext
from plotfunc import plot_func
from squaregrid import Squaregrid
from util import find_closest_half_point, merge_predicate
from windowmanager import WindowManager
from projection import project_point_line_2d
from lineprojectionview import LineProjection

WINDOWSIZE = (800, 800)
WINDOWCENTER = (WINDOWSIZE[0]/2, WINDOWSIZE[1]/2)
GRID_SUBDIVISIONS = (16,16)

sdl2.ext.init()

wm = WindowManager("Fibonacchitiling", WINDOWSIZE)

grid = Squaregrid(WINDOWSIZE, *GRID_SUBDIVISIONS)
grid.origin = WINDOWCENTER
grid.xyscale = np.array((50, -50))
projection = LineProjection((WINDOWSIZE[0], 100), (0, WINDOWSIZE[1] - 100))
projection.xyscale = np.array((50, 1))
projection.origin = np.array((400, 50))

PHI = (1+math.sqrt(5)) / 2
incline = -1/PHI
inclinescale = 0.0
offset = 0.0
offsetscale = 0.0


def get_f(incline:float, offset:float):
    return lambda x: incline*x+offset


def get_inv_f(incline:float, offset:float):
    return lambda x: (x-offset)/incline


def get_lattice_pts(startxy, endxy, func, invfunc):
    startx, starty = startxy
    endx, endy = endxy
    ydirection = int(math.copysign(1, func(endx) - func(startx)))
    xvals = np.fromiter(range(startx, endx+1), int)
    yvals = np.fromiter(range(starty, endy+ydirection, ydirection), int)
    x_pts = np.array([xvals, np.apply_along_axis(func, 0, xvals)]).transpose()
    y_pts = np.array([np.apply_along_axis(invfunc, 0, yvals), yvals]).transpose()
    pts = merge_predicate(lambda p1,p2: p1[0] < p2[0], x_pts, y_pts, 0)
    lpts = np.zeros((len(pts)-1,2))
    for i in range(len(pts)-1):
        halfway = (pts[i+1] + pts[i])/2
        grid.draw_dot_transformed(halfway, 3)
        lpts[i] = find_closest_half_point(halfway)
    return lpts


def draw_pt_proj_between(target:Squaregrid, p:np.ndarray, a:np.ndarray, b:np.ndarray):
    """Draw a line between `p` and the orthognal from `a` to `b`."""
    pp = project_point_line_2d(p, a, b-a)
    target.draw_line_transformed(p, pp)


def tickmethod():
    global incline, offset
    incline += inclinescale * 0.005
    offset += offsetscale * 0.05
    sdl2.SDL_SetRenderDrawColor(grid.renderer,0,0,0,0)
    sdl2.SDL_RenderClear(grid.renderer)
    f, inv_f = get_f(incline, offset), get_inv_f(incline, offset)
    xmin, xmax = -10, 10
    lpts = get_lattice_pts((xmin,int(f(xmin))), (xmax,int(f(xmax))), f, inv_f)
    for lpt in lpts:
        grid.draw_dot_transformed(lpt, 6)
    minxy,maxxy = np.array([xmin,f(xmin)]), np.array([xmax, f(xmax)])
    proj_lattice_pts = [project_point_line_2d(p, minxy, maxxy-minxy) for p in lpts]
    plot_func(grid, np.linspace(xmin,xmax,2), f)
    for i in range(len(lpts)):
        grid.draw_line_transformed(lpts[i], proj_lattice_pts[i])
    projection.hor_segments.clear()
    projection.vert_segments.clear()
    projection.projection_center[1] = offset
    for i,lpt in enumerate(lpts[1:],1):
        diff = lpt - lpts[i-1]
        if diff[0] == 0:
            projection.hor_segments.append((proj_lattice_pts[i-1], proj_lattice_pts[i]))
        else:
            projection.vert_segments.append((proj_lattice_pts[i-1], proj_lattice_pts[i]))
    projection.draw_pts()
    grid.draw(wm.renderer)
    projection.draw(wm.renderer)
    sdl2.SDL_RenderPresent(grid.renderer)


def rot_cw(event):
    global inclinescale
    if event.type == sdl2.SDL_KEYDOWN:
        inclinescale = -1.0
        return
    inclinescale = 0.0


def rot_ccw(event):
    global inclinescale
    if event.type == sdl2.SDL_KEYDOWN:
        inclinescale = 1.0
        return
    inclinescale = 0.0


def move_up(event):
    global offsetscale
    if event.type == sdl2.SDL_KEYDOWN:
        offsetscale = 1.0
        return
    offsetscale = 0.0


def move_down(event):
    global offsetscale
    if event.type == sdl2.SDL_KEYDOWN:
        offsetscale = -1.0
        return
    offsetscale = 0.0

wm.tickmethod = tickmethod
wm.set_key_event(sdl2.keycode.SDLK_LEFT, rot_ccw)
wm.set_key_event(sdl2.keycode.SDLK_RIGHT, rot_cw)
wm.set_key_event(sdl2.keycode.SDLK_DOWN, move_down)
wm.set_key_event(sdl2.keycode.SDLK_UP, move_up)
wm.run()
