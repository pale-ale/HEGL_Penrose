import sdl2.ext
import sdl2
import grid
from sprite import BaseSprite
import math
import numpy as np
import sdl2.sdlgfx as gfx
from util import iarray


class Squaregrid(BaseSprite):
    def __init__(self, size, subdivisionsx:int, subdivisionsy:int) -> None:
        super().__init__(size)
        self.verticalGrid = grid.Grid(size, subdivisionsx, (0, 0, 255, 255))
        self.verticalGrid.angle = math.pi/2
        self.horizontalGrid = grid.Grid(size, subdivisionsy, (255, 0, 0, 255))
        self.texture = None
        self.xyscale = np.array([1,1])
        self.origin = np.array([0,0])

    def draw(self, target:sdl2.ext.Renderer):
        self.horizontalGrid.draw(target)
        self.verticalGrid.draw(target)
        sdl2.SDL_RenderPresent(self.renderer)
        self.texture = sdl2.ext.Texture(target, self.surface)
        target.blit(self.texture)

    def transform_point_pixel(self, p):
        return iarray(self.xyscale * p + self.origin)

    def draw_line_transformed(self, start, end, color=(255,255,255,255)):
        gfx.lineRGBA(self.renderer, *self.transform_point_pixel(start), *self.transform_point_pixel(end), *color)

    def draw_box_transformed(self, topleft, size, color=(255,0,255,255)):
        tftl = iarray(self.xyscale * topleft + self.origin)
        sdl2.SDL_SetRenderDrawBlendMode(self.renderer, sdl2.SDL_BLENDMODE_NONE)
        gfx.boxRGBA(self.renderer, *(tftl), tftl[0] + size-1, tftl[1] + size-1, *color)

    def draw_dot_transformed(self, pos, radius, color=(0,255,255,255)):
        tfpos = iarray(self.xyscale * pos + self.origin)
        sdl2.SDL_SetRenderDrawBlendMode(self.renderer, sdl2.SDL_BLENDMODE_NONE)
        gfx.filledCircleRGBA(self.renderer, *(tfpos), radius, *color)
