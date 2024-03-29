import sdl2
import sdl2.ext
from typing import Callable
import ctypes
from sprite import BaseSprite
import numpy as np
import os
from PIL import Image


class WindowManager:
    """
    The WindowManager creates and manages the window, forwards events,
    and calls the event loop a given number of times per second.
    """
    def __init__(self, title:str, size:tuple[int,int], *windowargs) -> None:
        sdl2.ext.init()
        self.framerate = 30
        self.eventdict = dict()
        self.exiting = False
        self.paused = False
        self.tickmethod:Callable[[],None]|None = None
        self.ticks = 0
        self.window = sdl2.ext.Window(title, size, *windowargs)
        self.window.show()
        self.renderer = sdl2.ext.Renderer(self.window)
        self.set_key_event(sdl2.keycode.SDLK_SPACE, self.pause)
        self.tickdisplay = BaseSprite((50,10))
        self.capturing = False
        self.capturefolder = None
        self.capturedframes:list[str] = []

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
            frametime = newticks - self.ticks
            sdl2.SDL_RenderClear(self.tickdisplay.renderer, 0,0,0)
            self.tickdisplay.draw_text_transformed(np.array([3, 3]), f"{round(1000/frametime)}")
            self.tickdisplay.draw(self.renderer)
            self.renderer.present()
            self.window.refresh()
            remainingticks = int(max(1000/self.framerate - frametime, 0))
            sdl2.timer.SDL_Delay(remainingticks)
            self.ticks = newticks
            if self.capturing and self.capturefolder is not None and self.capturetarget is not None:
                filename = f"{len(self.capturedframes)}.bmp"
                sdl2.SDL_SaveBMP(self.capturetarget, (self.capturefolder + filename).encode('ascii'))
                self.capturedframes.append(filename)

    def pause(self, event):
        """
        Prevents the tickmethod from being called. 
        Call pause() again to continue.
        """
        if event.type == sdl2.SDL_KEYDOWN:
            self.paused = not self.paused

    def exit(self):
        """ Quit the next time we tick again, so cleanups can finish. """
        self.exiting = True
    
    def startcapture(self, target:sdl2.surface.SDL_Surface):
        self.capturefolder = f"{os.curdir}{os.sep}ImageCapture{os.sep}"
        os.makedirs(self.capturefolder, exist_ok=True)
        self.capturing = True
        self.capturetarget = target
    
    def combine_images_to_gif(self):
        if not self.capturefolder:
            return
        images = [Image.open(self.capturefolder + imagefilename) for imagefilename in self.capturedframes]
        outfilepath = self.capturefolder + "anim.gif"
        im = Image.new('RGBA',  self.window.size, (0,0,0,255))
        im.save(outfilepath, save_all=True, append_images=images)
    
    def cleanup_images(self):
        for imagepath in self.capturedframes:
            assert self.capturefolder is not None and imagepath.endswith(".bmp")
            os.remove(self.capturefolder + imagepath)

    def stopcapture(self):
        self.capturing = False
        self.combine_images_to_gif()
        self.cleanup_images()
