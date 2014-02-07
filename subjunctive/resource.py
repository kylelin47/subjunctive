import os.path

import sdl2.ext

_paths = [os.path.dirname(__file__)]

def add_path(path):
    _paths.append(path)

def image(name):
    for path in _paths:
        try:
            surface = sdl2.ext.load_image(os.path.join(path, name))
        except sdl2.ext.common.SDLError:
            pass
        else:
            return surface
    raise KeyError("image %r could not be found" % name)
