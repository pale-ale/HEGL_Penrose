from windowmanager import WindowManager
from pentagrid import Pentagrid
import numpy as np
import ctypes
import sdl2

def main():
    screensize = (1400, 800)
    pg = Pentagrid(screensize)
    wm = WindowManager("Penrose tiling", screensize)
    lattice_movement = np.zeros(5)
    grid_funkyness = 1.0 + 0j
    speed = 1/50

    def tickmethod():
        # breaks the sum of gamma == zero condition
        pg.mathpg.penrosemap.gamma += lattice_movement
        pg.mathpg.penrosemap.update_values(grid_funkyness)
        pg.draw(wm.renderer)
        # if grid_funkyness < 2:
        #     inc_funkyness(None)
        # else:
        #     wm.stopcapture()
        #     exit()
    
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
    
    def inc_real_funkyness(_): nonlocal grid_funkyness; grid_funkyness += speed * .3
    def dec_real_funkyness(_): nonlocal grid_funkyness; grid_funkyness -= speed * .3
    def inc_imag_funkyness(_): nonlocal grid_funkyness; grid_funkyness += speed * .3j
    def dec_imag_funkyness(_): nonlocal grid_funkyness; grid_funkyness -= speed * .3j
    def reset_imag_funkyness(_): nonlocal grid_funkyness; grid_funkyness = complex(grid_funkyness.real, 0)
    def start_stop_capture(event:sdl2.SDL_Event):
        if event.type == sdl2.events.SDL_KEYDOWN:
            nonlocal wm
            wm.stopcapture() if wm.capturing else wm.startcapture(pg.surface); 
            print(wm.capturing)

    wm.set_key_event(sdl2.keycode.SDLK_1, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_2, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_3, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_4, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_5, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_UP,    inc_real_funkyness)
    wm.set_key_event(sdl2.keycode.SDLK_DOWN,  dec_real_funkyness)
    wm.set_key_event(sdl2.keycode.SDLK_LEFT,  inc_imag_funkyness)
    wm.set_key_event(sdl2.keycode.SDLK_SPACE, reset_imag_funkyness)
    wm.set_key_event(sdl2.keycode.SDLK_RIGHT, dec_imag_funkyness)
    wm.set_key_event(sdl2.keycode.SDLK_RETURN, start_stop_capture)

    #wm.startcapture(pg.surface)
    wm.run()


if __name__ == "__main__":
    main()