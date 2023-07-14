from windowmanager import WindowManager
from pentagrid import Pentagrid
import numpy as np
import sdl2

def main():
    screensize = (1400, 800)
    pg = Pentagrid(screensize)
    wm = WindowManager("Penrose tiling", screensize)
    lattice_movement = np.zeros(5)
    params   = [0, 3, 3.1, 4.5, 6.1]
    # params   = [0, 2*np.pi/5, 4*np.pi/5, 6*np.pi/5, 8*np.pi/5]
    speed = 1/50

    def tickmethod():
        # breaks the sum of gamma == zero condition
        pg.mathpg.penrosemap.gamma += lattice_movement
        pg.mathpg.penrosemap.update_values(*params)
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
    
    def change_lattice_param(keyevent:sdl2.SDL_Event):
        nonlocal params
        keycodes = [
            sdl2.keycode.SDLK_q,
            sdl2.keycode.SDLK_w,
            sdl2.keycode.SDLK_e,
            sdl2.keycode.SDLK_r,
            sdl2.keycode.SDLK_t,
        ]
        if keyevent.type == sdl2.events.SDL_KEYDOWN:
            arr = np.array([(speed if keyevent.key.keysym.sym == keycode else 0.0) for keycode in keycodes])
            if keyevent.key.keysym.mod & sdl2.keycode.SDLK_LSHIFT:
                params -= arr
            else:
                params += arr
        #print(params)
    
    def start_stop_capture(event:sdl2.SDL_Event):
        if event.type == sdl2.events.SDL_KEYDOWN:
            nonlocal wm
            wm.stopcapture() if wm.capturing else wm.startcapture(pg.surface); 

    wm.set_key_event(sdl2.keycode.SDLK_1, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_2, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_3, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_4, change_movement)
    wm.set_key_event(sdl2.keycode.SDLK_5, change_movement)

    wm.set_key_event(sdl2.keycode.SDLK_q, change_lattice_param)
    wm.set_key_event(sdl2.keycode.SDLK_w, change_lattice_param)
    wm.set_key_event(sdl2.keycode.SDLK_e, change_lattice_param)
    wm.set_key_event(sdl2.keycode.SDLK_r, change_lattice_param)
    wm.set_key_event(sdl2.keycode.SDLK_t, change_lattice_param)

    wm.set_key_event(sdl2.keycode.SDLK_RETURN, start_stop_capture)

    wm.run()


if __name__ == "__main__":
    main()