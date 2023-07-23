""" Contains the SquareGrid class. """
import math

import sdl2
import sdl2.ext

from penroseGenerator.src.fibonacci.grid import Grid
from penroseGenerator.src.core.sprite import BaseSprite


class Squaregrid(BaseSprite):
    """ Contains two grids, oriented 90° to eachother. """
    def __init__(self, size, subdivisionsx:int, subdivisionsy:int) -> None:
        super().__init__(size)
        self.vertical_grid = Grid(size, subdivisionsx, (0, 0, 255, 255))
        self.vertical_grid.angle = math.pi/2
        self.horizontal_grid = Grid(size, subdivisionsy, (255, 0, 0, 255))
        self.texture = None

    def draw(self, target:sdl2.ext.Renderer):
        self.horizontal_grid.draw(target)
        self.vertical_grid.draw(target)
        sdl2.SDL_RenderPresent(self.renderer)
        self.texture = sdl2.ext.Texture(target, self.surface)
        target.blit(self.texture)

    def generate_labels(self):
        """ Label the axes. """
        for grid in [self.horizontal_grid, self.vertical_grid]:
            grid.xyscale = self.xyscale
            grid.origin = self.origin
            grid.generate_labels()
