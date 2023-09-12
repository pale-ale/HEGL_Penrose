""" Contains the BaseSprite class. """

import sdl2
import sdl2.ext
import sdl2.sdlgfx as gfx
import numpy as np

from penroseGenerator.src.core.geometrysurface import GeometrySurface


class BaseSprite(GeometrySurface):
    """ Allows simple sprite-based behaviour. """

    def __init__(self, size:tuple[int,int], position:tuple[int,int]=(0,0)):
        self.surface = sdl2.SDL_CreateRGBSurface(0, *size, 32,
                                   0xff000000,  # r mask
                                   0x00ff0000,  # g mask
                                   0x0000ff00,  # b mask
                                   0x000000ff)  # a mask
        self.renderer = sdl2.render.SDL_CreateSoftwareRenderer(self.surface)
        self.position = position
        self.xyscale = np.array([1,1])
        self.origin = np.array(size) * .5
        self.size = np.array(size)

    def draw(self, target:sdl2.ext.Renderer):
        """ Draw the sprite to a render target. """
        sdl2.SDL_RenderPresent(self.renderer)
        texture = sdl2.ext.Texture(target, self.surface)
        target.blit(texture, dstrect = sdl2.SDL_Rect(*self.position, *self.size))

    def transform_point_pixel(self, point):
        """ Transform a point into screen space. """
        x,y = (self.xyscale * (point + self.origin)).astype(np.int16)
        return np.array([x, self.size[1] - y])

    #pylint: disable=missing-function-docstring
    def draw_line_transformed(self, start, end, width=1, color=(255,255,255,255)):
        gfx.thickLineRGBA(
            self.renderer,
            *self.transform_point_pixel(start),
            *self.transform_point_pixel(end),
            width,
            *color
        ) # type: ignore

    def draw_dot_transformed(self, pos, radius, color=(0,255,255,255)):
        tfpos = self.transform_point_pixel(pos)
        sdl2.SDL_SetRenderDrawBlendMode(self.renderer, sdl2.SDL_BLENDMODE_NONE)
        gfx.filledCircleRGBA(self.renderer, *(tfpos), radius, *color) # type: ignore

    def draw_text_transformed(self, pos, text:str, color=(255,255,255,255)):
        tfpos = self.transform_point_pixel(pos)
        sdl2.SDL_SetRenderDrawBlendMode(self.renderer, sdl2.SDL_BLENDMODE_NONE)
        gfx.stringRGBA(self.renderer, *(tfpos), text.encode("ascii"), *color) # type: ignore

    def draw_box_transformed(self, topleft, size, color=(255,0,255,255)):
        tftl = self.transform_point_pixel(topleft)
        sdl2.SDL_SetRenderDrawBlendMode(self.renderer, sdl2.SDL_BLENDMODE_NONE)
        gfx.boxRGBA(self.renderer, *(tftl), tftl[0] + size-1, tftl[1] + size-1, *color) # type: ignore
