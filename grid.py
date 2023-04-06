import sdl2
import sdl2.ext
import sprite
import math


class Grid(sprite.BaseSprite):
    def __init__(self, size:tuple[int,int], subdivisions:int, color=(255,0,0,255)) -> None:
        self.size = size
        self.subdivisions = subdivisions
        super().__init__(size)
        self.color = color
        self.angle = 0
        self.texture = None
        for p1, p2 in self.get_pairs():
            sdl2.SDL_SetRenderDrawColor(self.renderer, *self.color)
            sdl2.SDL_RenderDrawLine(self.renderer, *p1, *p2)

    def get_pairs(self):
        xmax, ymax = self.size[0]-1, self.size[1]-1
        yield (0, 0), (xmax, 0)
        for i in range(self.subdivisions):
            y = i*self.size[1]/self.subdivisions
            yield (0, int(y)), (xmax, int(y))
        yield (0, ymax), (xmax, ymax)

    def draw(self, target:sdl2.ext.Renderer):
        if not self.texture:
            self.texture = sdl2.ext.Texture(target, self.surface)
        dstw, dsth = target.rendertarget.size
        dstpos = (int((dstw - self.size[0])/2), int((dsth - self.size[1])/2))
        target.blit(self.texture, dstrect=(dstpos), angle=math.degrees(self.angle))
