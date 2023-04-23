import sdl2.ext
import sdl2
import abc
import numpy as np
import sdl2.sdlgfx as gfx
from geometrysurface import GeometrySurface


class BaseSprite(GeometrySurface):
    def __init__(self, size:tuple[int,int], position:tuple[int,int]=(0,0)):
        self.surface = sdl2.SDL_CreateRGBSurface(0, *size, 32,
                                   0xff000000,  # r mask
                                   0x00ff0000,  # g mask
                                   0x0000ff00,  # b mask
                                   0x000000ff)  # a mask
        self.renderer = sdl2.render.SDL_CreateSoftwareRenderer(self.surface)
        self.position = position
        self.xyscale = np.array([1,1])
        self.origin = np.array([0,0])

    @abc.abstractmethod
    def draw(self, target:sdl2.ext.Renderer):
        pass

    def transform_point_pixel(self, p):
        return (self.xyscale * p + self.origin).astype(np.int16)

    def draw_line_transformed(self, start, end, color=(255,255,255,255)):
        gfx.lineRGBA(self.renderer, *self.transform_point_pixel(start), *self.transform_point_pixel(end), *color)

    def draw_dot_transformed(self, pos, radius, color=(0,255,255,255)):
        tfpos = (self.xyscale * pos + self.origin).astype(np.int16)
        sdl2.SDL_SetRenderDrawBlendMode(self.renderer, sdl2.SDL_BLENDMODE_NONE)
        gfx.filledCircleRGBA(self.renderer, *(tfpos), radius, *color)

    def draw_box_transformed(self, topleft, size, color=(255,0,255,255)):
        tftl = (self.xyscale * topleft + self.origin).astype(np.int16)
        sdl2.SDL_SetRenderDrawBlendMode(self.renderer, sdl2.SDL_BLENDMODE_NONE)
        gfx.boxRGBA(self.renderer, *(tftl), tftl[0] + size-1, tftl[1] + size-1, *color)