''' Entry point for the Penrose tiling '''

import numpy as np
import sdl2
from penroseGenerator.src.core.windowmanager import WindowManager
from penroseGenerator.src.penrose.pentagrid import Pentagrid

def main():
    ''' Open a window and draw a Penrose tiling. '''
    screensize = (1400, 800)
    pentagrid = Pentagrid(([int(1 * i) for i in screensize]))
    windowmanager = WindowManager("Penrose tiling", screensize)
    gamma_movement = np.zeros(5)
    zeta_movement = np.zeros(5)
    camera_movement = np.zeros(2)
    speed = 1/50

    def tickmethod():
        pentagrid.mathpg.penrosemap.gamma += gamma_movement
        pentagrid.mathpg.penrosemap.c_to_r5_factor += zeta_movement
        pentagrid.origin += camera_movement
        pentagrid.draw(windowmanager.renderer)

    windowmanager.tickmethod = tickmethod

    def change_movement(keyevent:sdl2.SDL_Event):
        nonlocal gamma_movement
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
                gamma_movement = -arr
            else:
                gamma_movement = arr
        else:
            gamma_movement = np.zeros(5)

    def change_lattice_param(keyevent:sdl2.SDL_Event):
        nonlocal zeta_movement
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
                zeta_movement = -arr
            else:
                zeta_movement = arr
        else:
            zeta_movement = np.zeros(5)

    def change_camera_movement(keyevent:sdl2.SDL_Event):
        nonlocal camera_movement
        if keyevent.type != sdl2.events.SDL_KEYDOWN:
            camera_movement = np.zeros(2)
            return
        if keyevent.key.keysym.sym == sdl2.keycode.SDLK_LEFT:
            camera_movement[0] =  speed * 5
        if keyevent.key.keysym.sym == sdl2.keycode.SDLK_RIGHT:
            camera_movement[0] = -speed * 5
        if keyevent.key.keysym.sym == sdl2.keycode.SDLK_UP:
            camera_movement[1] = -speed * 5
        if keyevent.key.keysym.sym == sdl2.keycode.SDLK_DOWN:
            camera_movement[1] =  speed * 5

    def start_stop_capture(event:sdl2.SDL_Event):
        if event.type == sdl2.events.SDL_KEYDOWN:
            nonlocal windowmanager
            if windowmanager.capturing:
                windowmanager.stopcapture()
            else:
                windowmanager.startcapture(pentagrid.surface)

    def inflate(event):
        if event.type == sdl2.events.SDL_KEYDOWN:
            pentagrid.mathpg.penrosemap.inflate()

    def deflate(event):
        if event.type == sdl2.events.SDL_KEYDOWN:
            pentagrid.mathpg.penrosemap.deflate()

    controltext = [
        "Enter : Start/Stop scene capture"
        "",
        "",
        "=========== Grid Controls ==========",
        "1-5         : Increase gammas 1-5",
        "Shift + 1-5 : Decrease gammas 1-5",
        "",
        "q,w,e,r,t         : Rotate zetas CW",
        "Shift + q,w,e,r,t : Rotate zetas CCW",
        "",
        "+           : Inflate",
        "-           : Deflate",
        "",
        "",
        "========== Camera Controls =========",
        ", (Comma)   : Zoom in",
        ". (Period)  : Zoom out",
        "",
        "Left/Right  : Move camera Left/Right",
        "Up/Down     : Move camera Up/Down",
    ]

    windowmanager.set_key_event(sdl2.keycode.SDLK_1, change_movement)
    windowmanager.set_key_event(sdl2.keycode.SDLK_2, change_movement)
    windowmanager.set_key_event(sdl2.keycode.SDLK_3, change_movement)
    windowmanager.set_key_event(sdl2.keycode.SDLK_4, change_movement)
    windowmanager.set_key_event(sdl2.keycode.SDLK_5, change_movement)

    windowmanager.set_key_event(sdl2.keycode.SDLK_q, change_lattice_param)
    windowmanager.set_key_event(sdl2.keycode.SDLK_w, change_lattice_param)
    windowmanager.set_key_event(sdl2.keycode.SDLK_e, change_lattice_param)
    windowmanager.set_key_event(sdl2.keycode.SDLK_r, change_lattice_param)
    windowmanager.set_key_event(sdl2.keycode.SDLK_t, change_lattice_param)

    windowmanager.set_key_event(sdl2.keycode.SDLK_LEFT,  change_camera_movement)
    windowmanager.set_key_event(sdl2.keycode.SDLK_RIGHT, change_camera_movement)
    windowmanager.set_key_event(sdl2.keycode.SDLK_UP,    change_camera_movement)
    windowmanager.set_key_event(sdl2.keycode.SDLK_DOWN,  change_camera_movement)

    windowmanager.set_key_event(sdl2.keycode.SDLK_COMMA, lambda _: pentagrid.add_zoom(np.array([.3,.3])))
    windowmanager.set_key_event(sdl2.keycode.SDLK_PERIOD, lambda _: pentagrid.add_zoom(-np.array([.3,.3])))

    windowmanager.set_key_event(sdl2.keycode.SDLK_PLUS, inflate)
    windowmanager.set_key_event(sdl2.keycode.SDLK_MINUS, deflate)

    windowmanager.set_key_event(sdl2.keycode.SDLK_RETURN, start_stop_capture)

    windowmanager.controls.controls.extend(controltext)

    windowmanager.run()


if __name__ == "__main__":
    main()
