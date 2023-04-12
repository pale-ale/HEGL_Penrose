from sprite import BaseSprite
import sdl2.ext
import sdl2
import numpy as np
import math


class LineProjection(BaseSprite):
    def __init__(self, size: tuple[int, int], position: tuple[int,int]):
        super().__init__(size, position)
        sdl2.SDL_SetRenderDrawColor(self.renderer, 50,75,75,255)
        sdl2.SDL_RenderClear(self.renderer)
        self.scolor = (200,  50,  50, 255)
        self.lcolor = ( 50, 100, 255, 255)
        self.texture = None
        self.vert_segments = []
        self.hor_segments = []
        self.projection_center = np.array([0,0])

    def _dir_dist(self, p, c):
        return math.copysign(np.linalg.norm(p-c), (p-c)[0])

    def draw_pts(self):
        sdl2.SDL_SetRenderDrawColor(self.renderer, 50,75,75,255)
        sdl2.SDL_RenderClear(self.renderer)
        if not self.texture:
            return
        self.draw_dot_transformed((0,0), 5, (0,0,0,255))
        for p1, p2 in self.hor_segments:
            start = self._dir_dist(p1, self.projection_center)
            end = self._dir_dist(p2, self.projection_center)
            self.draw_line_transformed((start, 0), (end, 0), self.scolor)
            self.draw_dot_transformed((start, 0), 2, (255,0,255,255))
            self.draw_dot_transformed((end, 0), 2, (255,0,255,255))
        for p1, p2 in self.vert_segments:
            start = self._dir_dist(p1, self.projection_center)
            end = self._dir_dist(p2, self.projection_center)
            self.draw_line_transformed((start, 0), (end, 0), self.lcolor)
            self.draw_dot_transformed((start, 0), 2, (255,0,255,255))
            self.draw_dot_transformed((end, 0), 2, (255,0,255,255))

    def draw(self, target: sdl2.ext.Renderer):
        sdl2.SDL_RenderPresent(self.renderer)
        self.texture = sdl2.ext.Texture(target, self.surface)
        target.blit(self.texture, (0,0,*self.texture.size), (*self.position, *self.texture.size))
