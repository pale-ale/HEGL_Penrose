import sdl2.ext
from sprite import BaseSprite
from numpy import ndarray, array, arange, outer, power, real, fromiter, inner, zeros
from math import pi, sqrt, e, ceil
from geometry import Line2D, intersect_line2D

class MathPentagrid():
    def __init__(self, gamma:ndarray) -> None:
        assert abs(sum(gamma)) <= 1e-10
        self.gamma = gamma
        self.xi = e ** (2j*pi/5)
        self.xis = power(array([self.xi]*5), (0,1,2,3,4))
        self.p = .5*(1 + sqrt(5))

    def is_on_grid(self, z:complex, j:int):
        assert 0 <= j <= 4
        tmp = (z * (self.xi**-j)).real + self.gamma[j]
        return abs(tmp - int(tmp)) <= 1e-10
    
    def reverse_is_on_grid(self, j:int, imin:int=-5, imax:int=5) -> list[Line2D]:
        ''' Return imax-imin of parameterized parallel lines representing the jth grid '''
        assert 0 <= j <= 4
        lines:list[Line2D] = []
        xi = self.xi**-j
        for i in range(imin, imax+1):
            line = Line2D(i + self.gamma[j], 0)
            line.direction = array([xi.real, xi.imag])
            lines.append(line)
        return lines
    
    def get_kj(self, z:complex, j:float):
        return ceil(real(z*self.xi**-j))
    
    def get_Ks(self, z:complex):
        return fromiter((self.get_kj(z, j) for j in range(5)), int, count=5)

    def k_times_xi(self, k:ndarray):
        return inner(k, self.xis)

class Pentagrid(BaseSprite):
    def __init__(self, size) -> None:
        super().__init__(size)
        self.mathpg = MathPentagrid(array([0,.1,.2,.3,-.6], float))   
        self.texture = None
        self.xyscale = array([50,50])
        self.origin = (self.size / self.xyscale) / 2

    def col(self, angle:float):
        full_red, full_green, full_blue = 0, pi, 2*pi
        def scalediff(f1:float,f2:float):
            return int(255 - (abs((f1-f2))/(2*pi))*255)
        rgb = [scalediff(angle,c) for c in [full_red, full_green, full_blue]]
        return (*rgb, 255)

    def intersect_linegroups(self, lg1:list[Line2D], lg2:list[Line2D]):
        intersections:list[ndarray] = []
        if lg1 == lg2:
            return []
        for line1 in lg1:
            for line2 in lg2:
                intersections.append(intersect_line2D(line1, line2)) # type: ignore
        return intersections

    def draw(self, target:sdl2.ext.Renderer):
        sdl2.SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 0)
        sdl2.SDL_RenderClear(self.renderer, 0,0,0)
        if True: # not self.texture:
            linegroups = [self.mathpg.reverse_is_on_grid(j, -5, 5) for j in range(5)]
            botleft = -self.size/(2*self.xyscale)
            topright = self.size/(2*self.xyscale)
            for linegroup in linegroups:
                for line in linegroup:
                    line.draw(self, botleft, topright, color=self.col(line.angle))
            # for linegroup in linegroups:
            #     for lg2 in linegroups:
            #         intersections = self.intersect_linegroups(linegroup, lg2)
            #         if intersections:
            #             for i in intersections:
            #                 self.draw_dot_transformed(i, 2, color=(0,255,255,100))
            self.draw_dot_transformed(array([0,0]), 3, (255,0,0,255))
            self.texture = sdl2.ext.Texture(target, self.surface)
        target.blit(self.texture)
