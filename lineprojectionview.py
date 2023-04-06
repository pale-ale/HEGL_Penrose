from sprite import BaseSprite
import sdl2.ext
import numpy as np

class LineProjection(BaseSprite):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.xpts = np.array([])
        self.ypts = np.array([])
        self.transformedxpts = np.array([])
        self.transformedypts = np.array([])
        self.renderer.draw_point()
    
    def update_pts(self, xpts, ypts):
        self.orderedpts = zip()

    def draw(self, target: sdl2.ext.Renderer):

        
