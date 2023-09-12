''' Contains the PentaGrid class '''

import numpy as np
import sdl2.ext
from penroseGenerator.src.core.geometry import Line2D, intersect_line2d, Lattice
from penroseGenerator.src.core.sprite import BaseSprite
from penroseGenerator.src.penrose.mathpentagrid import MathPentagrid
from penroseGenerator.src.penrose.penrosemaps import PenroseMap #pylint: disable=W0611

class Pentagrid(BaseSprite):
    ''' Draws and manages a pentagrid with its corresponding Penrose tiling. (Sort of...)'''

    def __init__(self, size) -> None:
        super().__init__(size)
        self.mathpg = MathPentagrid(PenroseMap(np.array([.0,.1,.2,.3,-.6], float)))
        self.texture = None
        self.xyscale = np.array([100,100], dtype=float)
        self.origin = (self.size / self.xyscale) / 2
        self.linecolors = [
            (255,  0,  0,255),
            (255,255,  0,255),
            (  0,255,  0,255),
            (  0,255,255,255),
            (  0,  0,255,255)]
        self.linemin, self.linemax = -1,1
        self.latticemax = 5

    def intersect_latices(self, lattice1:Lattice, lattice2:Lattice):
        ''' 
        Compute every intersection between two groups of evenly spaced, parallel lines.
        '''
        line1, start1, stop1, step1, offset1 = lattice1
        line2, start2, stop2, step2, offset2 = lattice2
        line1 = Line2D.copyconstruct(line1)
        line2 = Line2D.copyconstruct(line2)
        line1.dist_to_zero = start1 * step1 + offset1
        line2.dist_to_zero = start2 * step2 + offset2
        intersect0 = intersect_line2d(line1, line2)
        line1.dist_to_zero += step1
        intersect1 = intersect_line2d(line1 ,line2)
        line1.dist_to_zero -= step1
        line2.dist_to_zero += step2
        intersect2 = intersect_line2d(line1 ,line2)
        line2.dist_to_zero -= step2
        if intersect0 is None or intersect1 is None or intersect2 is None:
            return None
        lineno1 = stop1 - start1 + 1
        lineno2 = stop2 - start2 + 1
        dintersect1 = intersect1 - intersect0
        dintersect2 = intersect2 - intersect0
        lincomb1 = np.outer(np.arange(lineno1), dintersect1)
        lincomb2 = np.outer(np.arange(lineno2), dintersect2)
        intersects = intersect0 + lincomb1[None,:] + lincomb2[:,None]
        return np.reshape(intersects, (lineno1 * lineno2, 2))

    def get_intersections(self, lattices:list[Lattice]):
        ''' Return every intersection between the groups of evenly spaced, parallel lines. '''
        latticelines = self.linemax - self.linemin +1
        latticecount = len(lattices)
        intersectioncount = latticelines**2 * int(latticecount * (latticecount-1) / 2)
        intersections = np.zeros((intersectioncount, 4), dtype=float)
        index = 0
        for i, ilattice in enumerate(lattices):
            for j, jlattice in enumerate(lattices):
                if i >= j:
                    continue
                latt_inter = self.intersect_latices(ilattice, jlattice)
                licount = (ilattice[2] - ilattice[1] + 1) * (jlattice[2] - jlattice[1] + 1)
                if latt_inter is None:
                    continue
                intersections[index : index+licount, 0:2] = latt_inter
                intersections[index : index+licount, 2] = i
                intersections[index : index+licount, 3] = j
                index += licount
        return intersections

    def draw_penrose(self, lattices):
        ''' Draw a penrose tiling defined by `lattices`. '''
        intersections = self.get_intersections(lattices)
        for lattice_intersection in intersections:
            intersect, r, s = lattice_intersection[:2], *lattice_intersection[2:].astype(int)
            if r + s == 0:
                continue
            self.draw_dot_transformed(intersect, 4, color=self.linecolors[r])
            self.draw_dot_transformed(intersect, 2, color=self.linecolors[s])
            vertices = self.mathpg.get_verts_from_intersect(complex(*intersect), r, s)
            for i,vertex in enumerate(vertices):
                self.draw_line_transformed(vertices[i-1], vertex, width=5, color=self.linecolors[r])
                self.draw_line_transformed(vertices[i-1], vertex, width=2, color=self.linecolors[s])

    def add_zoom(self, zoom:np.ndarray):
        self.xyscale += zoom

    def draw(self, target:sdl2.ext.Renderer):
        sdl2.SDL_SetRenderDrawColor(self.renderer, 0,0,0,0)
        sdl2.SDL_RenderClear(self.renderer, 0,0,0)
        lattices = [
            self.mathpg.reverse_is_on_grid(
                j,
                self.linemin,
                self.linemax
            ) for j in range(self.latticemax)
        ]
        botleft = 5 * -self.size/(2*self.xyscale)
        topright = 5 * self.size/(2*self.xyscale)
        for i,lattice in enumerate(lattices):
            Line2D.draw_lattice(self, botleft, topright, lattice, color=(*self.linecolors[i][:-1], 200))
        self.draw_penrose(lattices)
        self.draw_dot_transformed(np.array([0,0]), 3, (255,0,0,255))
        self.texture = sdl2.ext.Texture(target, self.surface)
        target.blit(self.texture)
