import sdl2.ext
import grid
from sprite import BaseSprite
import math


class Pentagrid(BaseSprite):
    def __init__(self, sidelen:int, subdivisions:int) -> None:
        super().__init__((sidelen, sidelen))
        self.subgrids = [
            grid.Grid(sidelen, subdivisions, (255,   0,   0)),
            grid.Grid(sidelen, subdivisions, (255, 255,   0)),
            grid.Grid(sidelen, subdivisions, (  0, 255,   0)),
            grid.Grid(sidelen, subdivisions, (  0, 255, 255)),
            grid.Grid(sidelen, subdivisions, (  0,   0, 255))
        ]
        for i,g in enumerate(self.subgrids):
            g.angle = i * (2*math.pi)/5

    def draw(self, target:sdl2.ext.Renderer):
        for g in self.subgrids:
            g.draw(target)
