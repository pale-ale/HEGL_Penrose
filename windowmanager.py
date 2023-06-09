import sdl2
import sdl2.ext
from typing import Callable
import ctypes


class WindowManager:
    """
    The WindowManager creates and manages the window, forwards events,
    and calls the event loop a given number of times per second.
    """
    def __init__(self, *windowargs) -> None:
        self.framerate = 30
        self.eventdict = dict()
        self.exiting = False
        self.paused = False
        self.tickmethod:Callable[[None],None] = None
        self.ticks = 0
        self.window = sdl2.ext.Window(*windowargs)
        self.window.show()
        self.renderer = sdl2.ext.Renderer(self.window)
        self.set_key_event(sdl2.keycode.SDLK_SPACE, self.pause)

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
        """ "Tick" the program, update frame times, call the tickmethod. """
        self.exiting = False
        while not self.exiting:
            self.handle_events()
            if self.tickmethod and not self.paused:
                self.renderer.clear((0,0,0,255))
                self.tickmethod()
                self.renderer.present()
                self.window.refresh()
                newticks = sdl2.SDL_GetTicks()
                remainingticks = int(max(self.ticks + 1000/self.framerate - newticks, 0))
                sdl2.timer.SDL_Delay(remainingticks)
                self.ticks = newticks

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
