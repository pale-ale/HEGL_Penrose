''' Containts the WindowManager class. '''

import os
from typing import Callable

import ctypes
import sdl2
import sdl2.ext
from PIL import Image

from penroseGenerator.src.core.sprite import BaseSprite
from penroseGenerator.src.core.controls import Controls

CallbackType = Callable[[sdl2.SDL_Event], None]

class WindowManager:
    """
    The WindowManager creates and manages the window, forwards events,
    and calls the event loop a given number of times per second.
    """
    def __init__(self, title:str, size:tuple[int,int], *windowargs) -> None:
        sdl2.ext.init()
        fontpath = os.path.realpath(__file__ + "/../../../FreeMonoBold.ttf")
        self.fontmanager = sdl2.ext.FontManager(fontpath)
        self.framerate = 30
        self.eventdict:dict[int, CallbackType] = dict()
        self.exiting = False
        self.paused = False
        self.tickmethod : "Callable[[],None]|None" = None
        self.ticks = 0
        self.window = sdl2.ext.Window(title, size, *windowargs)
        self.window.show()
        self.renderer = sdl2.ext.Renderer(self.window)
        self.tickdisplay = BaseSprite((20,20), (10,10))
        self.capturing = False
        self.capturefolder = None
        self.capturetarget = None
        self.capturedframes:list[str] = []
        self.show_controls = True
        controls_width = 300
        controls_size = (controls_width, self.window.size[1])
        controls_pos =  (self.window.size[0] - controls_width, 0)
        self.controls = Controls(controls_size, controls_pos)
        self.set_key_event(sdl2.keycode.SDLK_SPACE, self.pause)
        self.set_key_event(sdl2.keycode.SDLK_h, self.toggle_controls)
        self.controls.controls = ["Space: Pause", "h: show/hide controls"]

    def set_key_event(self, key:int, callback:Callable[[sdl2.SDL_Event],None]):
        """ Set the callback for key `key` to `callback`. """
        self.eventdict[key] = callback

    def handle_key_event(self, event):
        """ Call the callbacks registered for they key event `event`. """
        if event.key.keysym.sym in self.eventdict:
            self.eventdict[event.key.keysym.sym](event)

    def handle_events(self):
        """ Poll events and handle them. """
        event = sdl2.events.SDL_Event()
        while sdl2.events.SDL_PollEvent(ctypes.byref(event), 1) == 1:
            match event.type:
                case sdl2.events.SDL_KEYDOWN | sdl2.events.SDL_KEYUP:
                    self.handle_key_event(event)
                case sdl2.events.SDL_QUIT:
                    self.exit()

    def run(self):
        """ Hand over execution flow to the WindowManager which calls the "tickmethod". """
        self.exiting = False
        if not self.tickmethod:
            print("No tickmethod assigned. Exiting...")
            exit()
        while not self.exiting:
            self.handle_events()
            if self.paused:
                return
            self.renderer.clear((0,0,0,255))
            self.tickmethod()
            newticks = sdl2.SDL_GetTicks()
            frametime = max(1, newticks - self.ticks)
            sdl2.SDL_RenderClear(self.tickdisplay.renderer, 0,0,0)
            self.tickdisplay.surface = self.fontmanager.render(str(round(frametime)).zfill(2), size=20)
            self.tickdisplay.draw(self.renderer)
            if self.show_controls:
                self.controls.draw(self.renderer)
            self.renderer.present()
            remainingticks = int(max(1000/self.framerate - frametime, 0))
            sdl2.timer.SDL_Delay(remainingticks)
            self.ticks = newticks
            if self.capturing and self.capturefolder is not None and self.capturetarget is not None:
                filename = f"{len(self.capturedframes)}.bmp"
                sdl2.SDL_SaveBMP(self.capturetarget, (self.capturefolder + filename).encode('ascii'))
                self.capturedframes.append(filename)
            self.window.refresh()

    def pause(self, event):
        """
        Prevents the tickmethod from being called. 
        Call pause() again to continue.
        """
        if event.type == sdl2.SDL_KEYDOWN:
            self.paused = not self.paused

    def toggle_controls(self, keyevent:sdl2.SDL_Event):
        """ Display/Hide the configured callbacks on screen. """
        if keyevent.type == sdl2.events.SDL_KEYDOWN:
            self.show_controls = not self.show_controls

    def exit(self):
        """ Quit the next time we tick again, so cleanups can finish. """
        self.exiting = True

    def startcapture(self, target:sdl2.surface.SDL_Surface):
        """ Start taking snapshots of the window every tick. """
        self.capturefolder = f"{os.curdir}{os.sep}ImageCapture{os.sep}"
        os.makedirs(self.capturefolder, exist_ok=True)
        self.capturing = True
        self.capturetarget = target

    def stopcapture(self):
        """ Stop capturing and save to ImageCapture/anim.gif. """
        self.capturing = False
        self._combine_images_to_gif()
        self._cleanup_images()

    def _combine_images_to_gif(self):
        if not self.capturefolder:
            return
        images = [Image.open(self.capturefolder + filename) for filename in self.capturedframes]
        outfilepath = self.capturefolder + "anim.gif"
        image = Image.new('RGBA',  self.window.size, (0,0,0,255))
        image.save(outfilepath, save_all=True, append_images=images, transparency=255)

    def _cleanup_images(self):
        for imagepath in self.capturedframes:
            assert self.capturefolder is not None and imagepath.endswith(".bmp")
            os.remove(self.capturefolder + imagepath)
