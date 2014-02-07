import sdl2
import sdl2.ext

from . import grid
from . import entity
from . import resource
from . import world

def run(world, *, on_direction=None):
    while True:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                return
            elif event.type == sdl2.SDL_KEYDOWN:
                sym = event.key.keysym.sym
                if on_direction:
                    direction = grid.KEYBOARD.get(sym)
                    if direction:
                        on_direction(direction)
        world._draw()
        sdl2.timer.SDL_Delay(20)

sdl2.ext.init()
