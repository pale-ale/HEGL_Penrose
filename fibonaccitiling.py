import numpy as np
import sdl2
import sdl2.ext
from squaregrid import Squaregrid
from util import find_closest_half_point, merge_sorted_predicate
from windowmanager import WindowManager
from projection import project_point_line_2d
from lineprojectionview import LineProjection
from geometry import Line2D

WINDOWSIZE = (800, 800)
WINDOWCENTER = (WINDOWSIZE[0]/2, WINDOWSIZE[1]/2)
GRID_SUBDIVISIONS = (16, 16)

# Show/Hide visuals
SHOW_LINE = True
SHOW_HALFWAYS = True
SHOW_PROJECTIONS = True
SHOW_LATTICE_POINTS = True
SHOW_INTEGRALS = True

sdl2.ext.init()

wm = WindowManager("Fibonacchitiling", WINDOWSIZE)

grid = Squaregrid(WINDOWSIZE, *GRID_SUBDIVISIONS)
grid.xyscale = np.array((50, 50))
grid.origin = np.array([*WINDOWCENTER]) / grid.xyscale
grid.generate_labels()

projection = LineProjection((WINDOWSIZE[0], 100), (0, WINDOWSIZE[1] - 100))
projection.xyscale = np.array((50, 1))
projection.origin = np.array((400, 50)) / projection.xyscale

anglerate = 0.0
moverate = 0.0

line = Line2D(0, 0.553574)


def get_lattice_pts(line: Line2D, xmin, ymin, xmax, ymax):
    """
    For each square bounded by integers between xyminmax and 
    intersecting with `line`, return the center.
    """
    assert xmin <= xmax and ymin <= ymax
    lo, hi = np.array([xmin, ymin]), np.array([xmax, ymax])
    x_ts = line.get_int_values(0, lo, hi)
    y_ts = line.get_int_values(1, lo, hi)
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
    line.dist_to_zero += moverate * 0.05
    line.angle += anglerate * 0.005
    sdl2.SDL_SetRenderDrawColor(grid.renderer, 0, 0, 0, 0)
    sdl2.SDL_RenderClear(grid.renderer)
    minxy, maxxy = np.array([-5, -5]), np.array([5,5])
    lpts = get_lattice_pts(line,*minxy, *maxxy)
    if SHOW_LATTICE_POINTS:
        for lpt in lpts:
            grid.draw_dot_transformed(lpt, 6)
    proj_lattice_pts = [project_point_line_2d(p, line.start, line.direction) for p in lpts]
    if SHOW_LINE:
        line.draw(grid, minxy, maxxy)
    if SHOW_PROJECTIONS:
        for i in range(len(lpts)):
            grid.draw_line_transformed(lpts[i], proj_lattice_pts[i])
    projection.hor_segments.clear()
    projection.vert_segments.clear()
    projection.projection_center = line.normal * line.dist_to_zero
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
