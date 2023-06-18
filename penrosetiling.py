from windowmanager import WindowManager
from pentagrid import Pentagrid
import numpy as np
import sdl2

def main():
    screensize = (1400, 800)
    pg = Pentagrid(screensize)
    wm = WindowManager("Penrose tiling", screensize)
    lattice_movement = np.zeros(5)
    speed = 1/50

    def tickmethod():
        # breaks the sum of gamma == zero condition
        pg.mathpg.gamma += lattice_movement
        pg.draw(wm.renderer)
    
    wm.tickmethod = tickmethod

    def change_movement(keyevent:sdl2.SDL_Event):
        nonlocal lattice_movement
        keycodes = [
            sdl2.keycode.SDLK_1,
            sdl2.keycode.SDLK_2,
            sdl2.keycode.SDLK_3,
            sdl2.keycode.SDLK_4,
            sdl2.keycode.SDLK_5,
        ]
        if keyevent.type == sdl2.events.SDL_KEYDOWN:
            arr = np.array([(speed if keyevent.key.keysym.sym == keycode else 0.0) for keycode in keycodes])
            if keyevent.key.keysym.mod & sdl2.keycode.SDLK_LSHIFT:
                lattice_movement = -arr
            else:
                lattice_movement = arr
        else:
            lattice_movement = np.zeros(5)
    
    wm.set_key_event(sdl2.keycode.SDLK_1, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_2, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_3, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_4, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_5, change_movement)

    wm.run()


if __name__ == "__main__":
    main()