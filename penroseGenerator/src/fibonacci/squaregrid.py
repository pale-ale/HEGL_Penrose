import sdl2.ext
import sdl2
from src.fibonacci.grid import Grid
from sprite import BaseSprite
import math


class Squaregrid(BaseSprite):
    def __init__(self, size, subdivisionsx:int, subdivisionsy:int) -> None:
        super().__init__(size)
        self.verticalGrid = Grid(size, subdivisionsx, (0, 0, 255, 255))
        self.verticalGrid.angle = math.pi/2
        self.horizontalGrid = Grid(size, subdivisionsy, (255, 0, 0, 255))
        self.texture = None

    def draw(self, target:sdl2.ext.Renderer):
        self.horizontalGrid.draw(target)
        self.verticalGrid.draw(target)
        sdl2.SDL_RenderPresent(self.renderer)
        self.texture = sdl2.ext.Texture(target, self.surface)
        target.blit(self.texture)

    def generate_labels(self):
        for grid in [self.horizontalGrid, self.verticalGrid]:
            grid.xyscale = self.xyscale
            grid.origin = self.origin
            grid.generate_labels()
