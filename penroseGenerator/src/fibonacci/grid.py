""" Draws some lines and can perform transformations. """

import os
import math
import ctypes

import sdl2
import sdl2.ext
import sdl2.ext.ttf

from penroseGenerator.src.core.sprite import BaseSprite


class Grid(BaseSprite):
    """
    Use this class to create evenly spaced lines
    with transformations between coordinate systems.
    """

    def __init__(self, size: tuple[int, int], subdivisions: int, color=(255, 0, 0, 255)) -> None:
        self.size = size
        self.subdivisions = subdivisions
        super().__init__(size)
        self.color = color
        self.angle = 0.0
        self.texture = None
        for part1, part2 in self.get_pairs():
            sdl2.SDL_SetRenderDrawColor(self.renderer, *self.color)
            sdl2.SDL_RenderDrawLine(self.renderer, *part1, *part2)
        fontpaths = [
            "/usr/share/fonts/opentype/fira/FiraMono-Bold.otf",
            "C:\\Windows\\Fonts\\Arial.ttf",
            "/Library/Fonts/Arial.otf"
        ]
        self.font = None
        for fontpath in fontpaths:
            if os.path.exists(fontpath):
                self.font = sdl2.ext.FontTTF(
                    fontpath, 13, (255, 255, 255, 255))

    def get_pairs(self):
        """ Iterate over the (start, end) pair of each line. """
        xmax, ymax = self.size[0]-1, self.size[1]-1
        yield (0, 0), (xmax, 0)
        for i in range(self.subdivisions):
            ystep = i*self.size[1]/self.subdivisions
            yield (0, int(ystep)), (xmax, int(ystep))
        yield (0, ymax), (xmax, ymax)

    def generate_labels(self):
        """ 
        Create the numbers on an axis. 
        Uses the reverse transformation to get the numbers. 
        """
        if not self.font:
            return
        for part1, _ in self.get_pairs():
            label = -(part1[1] / self.xyscale[1] - self.origin[1])
            surf = self.font.render_text(str(label))
            tex = sdl2.SDL_CreateTextureFromSurface(self.renderer, surf)
            width, height = ctypes.c_int(), ctypes.c_int()
            sdl2.SDL_QueryTexture(tex, None, None, width, height)
            rect = sdl2.SDL_Rect(*part1, width, height)
            sdl2.SDL_RenderCopy(self.renderer, tex, None, rect)

    def draw(self, target: sdl2.ext.Renderer):
        """ Draw the grid onto the target renderer/surface. """
        if not self.texture:
            self.texture = sdl2.ext.Texture(target, self.surface)
        dstw, dsth = target.rendertarget.size
        dstpos = (int((dstw - self.size[0])/2), int((dsth - self.size[1])/2))
        target.blit(self.texture, dstrect=(dstpos),
                    angle=int(math.degrees(self.angle)))
