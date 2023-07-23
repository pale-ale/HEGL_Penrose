"""Contains the LineProjection class. """
import math

import sdl2
import sdl2.ext
import numpy as np

from penroseGenerator.src.core.sprite import BaseSprite


class LineProjection(BaseSprite):
    """ Projects some line to a seperate UI space. """
    def __init__(self, size: tuple[int, int], position: tuple[int, int]):
        super().__init__(size, position)
        sdl2.SDL_SetRenderDrawColor(self.renderer, 50, 75, 75, 255)
        sdl2.SDL_RenderClear(self.renderer)
        self.hcolor = (200,  50,  50, 255)
        self.vcolor = (50, 100, 255, 255)
        self.texture = None
        self.vert_segments = []
        self.hor_segments = []
        self.projection_center = np.array([0, 0])

    def _dir_dist(self, val1, val2):
        return math.copysign(np.linalg.norm(val1-val2), (val1-val2)[0])

    def draw_pts(self):
        """ Draw the points projected onto the line. """
        sdl2.SDL_SetRenderDrawColor(self.renderer, 50, 75, 75, 255)
        sdl2.SDL_RenderClear(self.renderer)
        if not self.texture:
            return
        self.draw_dot_transformed(np.zeros(2), 5, (0, 0, 0, 255))
        for point1, point2 in self.hor_segments:
            start = self._dir_dist(point1, self.projection_center)
            end = self._dir_dist(point2, self.projection_center)
            self.draw_line_transformed(np.array([start, 0]), np.array([end, 0]), color=self.hcolor)
            self.draw_dot_transformed( np.array([start, 0]), 2, (255, 0, 255, 255))
            self.draw_dot_transformed( np.array([end,   0]), 2, (255, 0, 255, 255))
        for point1, point2 in self.vert_segments:
            start = self._dir_dist(point1, self.projection_center)
            end = self._dir_dist(point2, self.projection_center)
            self.draw_line_transformed(np.array([start, 0]), np.array([end, 0]), color=self.vcolor)
            self.draw_dot_transformed( np.array([start, 0]), 2, (255, 0, 255, 255))
            self.draw_dot_transformed( np.array([end,   0]), 2, (255, 0, 255, 255))

    def draw(self, target: sdl2.ext.Renderer):
        sdl2.SDL_RenderPresent(self.renderer)
        self.texture = sdl2.ext.Texture(target, self.surface)
        target.blit(self.texture, (0, 0, *self.texture.size),
                    (*self.position, *self.texture.size))
