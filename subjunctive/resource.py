import logging
import os.path

import sdl2.ext
import sdl2.sdlmixer

from sdl2.ext.compat import byteify

_paths = [os.path.dirname(__file__)]
default_image = sdl2.ext.load_image(os.path.join(_paths[0],
                                    'images/default.png'))

def add_path(path):
    _paths.append(path)

def image(name):
    """Return an sdl surface containing the image with the given name

    Subjunctive keeps a list of resource paths that are searched; your
    application should add its path to this list by doing:

        subjunctive.resource.add_path(os.path.dirname(__file__))

    If the specified name cannot be found, the default image will be
    returned.
    """
    for path in _paths:
        try:
            surface = sdl2.ext.load_image(os.path.join(path, name))
        except sdl2.ext.common.SDLError:
            pass
        else:
            return surface
    logging.warning("image %r could not be found; using default" % name)
    return default_image

def music(name):
    for path in _paths:
        music = sdl2.sdlmixer.Mix_LoadMUS(byteify(os.path.join(path, name), 
                                          "utf-8"))
        try:
            music.contents
        except ValueError:
            pass
        else:
            return music

def file(name):
    for path in _paths:
        try:
            text = open(os.path.join(path, name))
        except FileNotFoundError:
            pass
        except PermissionError:
            logging.warning("Trying to access directory " + path + 
                            " with insufficient permission. " +
                            "Continuing search")
            pass
        else:
            return text
    raise FileNotFoundError
