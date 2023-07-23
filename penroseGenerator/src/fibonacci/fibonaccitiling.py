''' Draws a Fibonacci Tiling. '''

import sdl2
import sdl2.ext
import numpy as np

from penroseGenerator.src.core.util import find_closest_half_point, merge_sorted_predicate
from penroseGenerator.src.core.windowmanager import WindowManager
from penroseGenerator.src.core.geometry import Line2D, project_point_line_2d
from penroseGenerator.src.fibonacci.squaregrid import Squaregrid
from penroseGenerator.src.fibonacci.lineprojectionview import LineProjection

WINDOWSIZE = (800, 800)
WINDOWCENTER = (WINDOWSIZE[0]/2, WINDOWSIZE[1]/2)
GRID_SUBDIVISIONS = (16, 16)

# Show/Hide visuals
SHOW_LINE = True
SHOW_HALFWAYS = True
SHOW_PROJECTIONS = True
SHOW_LATTICE_POINTS = True
SHOW_INTEGRALS = True

LINE = Line2D(0, 0.553574)

sdl2.ext.init()

wm = WindowManager("Fibonacchitiling", WINDOWSIZE)

grid = Squaregrid(WINDOWSIZE, *GRID_SUBDIVISIONS)
grid.xyscale = np.array((50, 50))
grid.origin = np.array([*WINDOWCENTER]) / grid.xyscale
grid.generate_labels()

projection = LineProjection((WINDOWSIZE[0], 100), (0, WINDOWSIZE[1] - 100))
projection.xyscale = np.array((100, 1))
projection.origin = np.array((400, 50)) / projection.xyscale

anglerate = 0.0  #pylint: disable=invalid-name
moverate  = 0.0   #pylint: disable=invalid-name


def get_lattice_pts(line: Line2D, xmin, ymin, xmax, ymax):
    """
    For each square bounded by integers between xyminmax and 
    intersecting with `line`, return the center.
    """
    assert xmin <= xmax and ymin <= ymax
    lowest, highest = np.array([xmin, ymin]), np.array([xmax, ymax])
    x_ts = line.get_int_values(0, lowest, highest)
    y_ts = line.get_int_values(1, lowest, highest)
    for t in x_ts:
        grid.draw_dot_transformed(line(t), 4, (255, 0, 0, 255))
    for t in y_ts:
        grid.draw_dot_transformed(line(t), 4, (0, 255, 0, 255))
    ts = merge_sorted_predicate(lambda a, b: a < b, x_ts, y_ts)
    pts = np.array([line(t) for t in ts])
    lpts = np.zeros((len(pts)-1, 2))
    for i in range(len(pts)-1):
        halfway = (pts[i+1] + pts[i])/2
        if SHOW_HALFWAYS:
            grid.draw_dot_transformed(halfway, 4, (255, 0, 255, 255))
        lpts[i] = find_closest_half_point(halfway)
    return lpts


def draw_pt_proj_between(target: Squaregrid, p: np.ndarray, a: np.ndarray, b: np.ndarray):
    """Draw the shortest path between `p` and the line from `a` to `b`."""
    pp = project_point_line_2d(p, a, b-a)
    target.draw_line_transformed(p, pp)


def tickmethod():
    LINE.dist_to_zero += moverate * 0.05
    LINE.angle += anglerate * 0.005
    sdl2.SDL_SetRenderDrawColor(grid.renderer, 0, 0, 0, 0)
    sdl2.SDL_RenderClear(grid.renderer)
    minxy, maxxy = np.array([-10, -10]), np.array([10,10])
    lpts = get_lattice_pts(LINE,*minxy, *maxxy)
    if SHOW_LATTICE_POINTS:
        for lpt in lpts:
            grid.draw_dot_transformed(lpt, 6)
    proj_lattice_pts = [project_point_line_2d(p, LINE.start, LINE.direction) for p in lpts]
    if SHOW_LINE:
        LINE.draw(grid, minxy, maxxy)
    if SHOW_PROJECTIONS:
        for i, lpt in enumerate(lpts):
            grid.draw_line_transformed(lpt, proj_lattice_pts[i])
    projection.hor_segments.clear()
    projection.vert_segments.clear()
    projection.projection_center = LINE.normal * LINE.dist_to_zero
    for i, lpt in enumerate(lpts[1:], 1):
        diff = lpt - lpts[i-1]
        if diff[0] == 0:
            projection.hor_segments.append(
                (proj_lattice_pts[i-1], proj_lattice_pts[i]))
        else:
            projection.vert_segments.append(
                (proj_lattice_pts[i-1], proj_lattice_pts[i]))
    projection.draw_pts()
    sdl2.SDL_RenderPresent(grid.renderer)
    grid.draw(wm.renderer)
    projection.draw(wm.renderer)


def rot_cw(event):
    global anglerate
    if event.type == sdl2.SDL_KEYDOWN:
        anglerate = -1.0
        return
    anglerate = 0.0


def rot_ccw(event):
    global anglerate
    if event.type == sdl2.SDL_KEYDOWN:
        anglerate = 1.0
        return
    anglerate = 0.0


def move_orth_fwd(event):
    global moverate
    if event.type == sdl2.SDL_KEYDOWN:
        moverate = 1.0
        return
    moverate = 0.0


def move_orth_bwd(event):
    global moverate
    if event.type == sdl2.SDL_KEYDOWN:
        moverate = -1.0
        return
    moverate = 0.0


wm.tickmethod = tickmethod
wm.set_key_event(sdl2.keycode.SDLK_LEFT, rot_ccw)
wm.set_key_event(sdl2.keycode.SDLK_RIGHT, rot_cw)
wm.set_key_event(sdl2.keycode.SDLK_DOWN, move_orth_fwd)
wm.set_key_event(sdl2.keycode.SDLK_UP, move_orth_bwd)
wm.run()
