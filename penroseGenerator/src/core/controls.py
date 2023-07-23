""" Contains the Controls class. """

import sdl2
import sdl2.ext
import numpy as np

from penroseGenerator.src.core.sprite import BaseSprite

class Controls(BaseSprite):
    """ Allows displaying a text nicely in a vertical manner, used for keybindings. """
    def __init__(self, size: tuple[int, int], position: tuple[int, int]):
        super().__init__(size, position)
        sdl2.SDL_SetRenderDrawColor(self.renderer, 50, 75, 75, 255)
        sdl2.SDL_RenderClear(self.renderer)
        self.texture = None
        self.origin = np.array([0,self.size[1]])
        self.controls: list[str] = []

    def draw(self, target: sdl2.ext.Renderer):
        sdl2.SDL_SetRenderDrawColor(self.renderer, 50, 75, 75, 255)
        sdl2.SDL_RenderClear(self.renderer)
        for line,helptext in enumerate(self.controls):
            self.draw_text_transformed(np.array([5, -line * 15 - 5]), helptext)
        sdl2.SDL_RenderPresent(self.renderer)
        self.texture = sdl2.ext.Texture(target, self.surface)
        target.blit(self.texture, (0, 0, *self.texture.size),
                    (*self.position, *self.texture.size))
