import sdl2.ext
from sprite import BaseSprite
from numpy import ndarray, array, power, fromiter, inner, zeros
from math import pi, e, ceil
from geometry import Line2D, intersect_line2D
from mathpentagrid import MathPentagrid


class PerfPentagrid(BaseSprite):
    ''' Draws and manages a pentagrid with its corresponding Penrose tiling. (Sort of...)'''

    def __init__(self, size) -> None:
        super().__init__(size)
        self.mathpg = MathPentagrid(array([0,.1,.2,.3,-.6], float))   
        self.texture = None
        self.xyscale = array([50,50])
        self.origin = (self.size / self.xyscale) / 2

    def col(self, angle:float):
        ''' Returns a color for a given angle, used for drawing distinguishable lines. '''
        full_red, full_green, full_blue = 0, pi, 2*pi
        def scalediff(f1:float,f2:float):
            return int(255 - (abs((f1-f2))/(2*pi))*255)
        rgb = [scalediff(angle,c) for c in [full_red, full_green, full_blue]]
        return (*rgb, 255)

    def intersect_linegroup(self, lg1:Line2D, lg1step:float, lg2:Line2D, lg2step:float, xrange, yrange):
        ''' 
        Compute every intersection between two groups of evenly spaced, parallel lines.
        ### Parameters
        `lg1` and `lg2` represent a single line from each group.\ 
        `lg1step` and `lg2step` are the distances between each line from the respective group.\ 
        Use `xrange` and `yrange` to set the bounds for the linear combinations.
        '''
        if lg1 == lg2:
            return
        intersect0 = intersect_line2D(lg1 ,lg2)
        lg1.dist_to_zero += lg1step
        intersect1 = intersect_line2D(lg1 ,lg2)
        lg1.dist_to_zero -= lg1step
        lg2.dist_to_zero += lg2step
        intersect2 = intersect_line2D(lg1 ,lg2)
        lg2.dist_to_zero -= lg2step
        assert intersect0 is not None and intersect1 is not None and intersect2 is not None
        dintersect1 = intersect1 - intersect0
        dintersect2 = intersect2 - intersect0
        for y in yrange:
            for x in xrange:
                yield intersect0 + x * dintersect1 + y * dintersect2

    def get_intersections(self, linegroups:list[list[Line2D]]):
        ''' Return every intersection between the groups of evenly spaced, parallel lines. '''
        completed = set()
        intersections:list[tuple[ndarray, int ,int]] = []
        for i in range(len(linegroups)):
            for j in range(len(linegroups)):
                if (i,j) in completed or i == j:
                    continue
                completed.add((i,j))
                completed.add((j,i))
                l1 = linegroups[i][0]
                l2 = linegroups[j][0]
                for intersection in self.intersect_linegroup(l1, 1, l2, 1, range(len(linegroups[i])), range(len(linegroups[j]))):
                    intersections.append((intersection, i, j))
        return intersections

    def draw_penrose(self, linegroups):
        ''' Draw a penrose tiling defined by `linegroups`. '''
        intersections = self.get_intersections(linegroups)
        for intersect, r, s in intersections:
            assert self.mathpg.is_on_grid(complex(*intersect), r) and\
                self.mathpg.is_on_grid(complex(*intersect), s)
            self.draw_dot_transformed(intersect, 2)
            delta1 = zeros(5); delta1[r]=1
            delta2 = zeros(5); delta2[s]=1
            vertices = ndarray((4,2), float)
            es = [[0,0], [1,0], [1,1], [0,1]]
            for i,(e1,e2) in enumerate(es):
                ks = self.mathpg.get_Ks(complex(*intersect))
                vertex5d = ks + e1*delta1 + e2*delta2
                vertex2d = self.mathpg.k_times_xi(vertex5d)
                vertices[i:,] = array([vertex2d.real, vertex2d.imag])
            for i in range(len(vertices)):
                self.draw_line_transformed(vertices[i-1], vertices[i], (0,255,0,255))

    def draw(self, target:sdl2.ext.Renderer):
        sdl2.SDL_SetRenderDrawColor(self.renderer, 0,0,0,0)
        sdl2.SDL_RenderClear(self.renderer, 0,0,0)
        linemin, linemax = -1, 1
        linegroups = [self.mathpg.reverse_is_on_grid(j, linemin, linemax) for j in range(2)]
        botleft = -self.size/(2*self.xyscale)
        topright = self.size/(2*self.xyscale)
        for linegroup in linegroups:
            for line in linegroup:
                line.draw(self, botleft, topright, color=self.col(line.angle))
        self.draw_penrose(linegroups)
        self.draw_dot_transformed(array([0,0]), 3, (255,0,0,255))
        self.texture = sdl2.ext.Texture(target, self.surface)
        target.blit(self.texture)
