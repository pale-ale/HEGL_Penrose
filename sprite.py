import sdl2.ext
import sdl2
import abc


class BaseSprite(abc.ABC):
    def __init__(self, size:tuple[int,int]):
        self.surface = sdl2.SDL_CreateRGBSurface(0, *size, 32,
                                   0xff000000,  # r mask
                                   0x00ff0000,  # g mask
                                   0x0000ff00,  # b mask
                                   0x000000ff)  # a mask
        self.renderer = sdl2.render.SDL_CreateSoftwareRenderer(self.surface)

    @abc.abstractmethod
    def draw(self, target:sdl2.ext.Renderer):
        pass
