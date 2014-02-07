import os.path

import sdl2
import sdl2.ext

import subjunctive

subjunctive.resource.add_path(os.path.dirname(__file__))

class Planet(subjunctive.world.World):
    background = subjunctive.resource.image('images/whiteplane.png')
    grid = subjunctive.grid.Grid(12, 12)
    grid_offset = (0, 0)
    tile_size = (16, 16)
    window_caption = "Think Better"

    def __init__(self):
        super().__init__()

    def setup(self, cursor):
        self.place(cursor, self.center)
        self.spawn_random(BlueBlock, 20, edges=False)
        self.spawn_random(RedBlock, 20, edges=False)
        self.spawn_random(OrangeBlock, 20, edges=False)
        self.spawn_random(GreenBlock, 20, edges=False)

class Block(subjunctive.entity.Entity):
    image = subjunctive.resource.image('images/defaultblock.png')
    pushable = True
    antiblock = None

    def push(self, direction, pusher=None):
        if pusher.__class__.__name__ == self.antiblock:
            self.world.remove(pusher)
            self.world.remove(self)
        if isinstance(pusher, Cursor) or pusher.__class__ == self.__class__:
            self.move(direction)

class BlueBlock(Block):
    image = subjunctive.resource.image('images/blueblock.png')
    antiblock = "OrangeBlock"

class Cursor(subjunctive.entity.Entity):
    orientable = True
    image = subjunctive.resource.image('images/cursor.png')

class GreenBlock(Block):
    image = subjunctive.resource.image('images/greenblock.png')
    antiblock = "RedBlock"

class OrangeBlock(Block):
    image = subjunctive.resource.image('images/orangeblock.png')
    antiblock = "BlueBlock"

class RedBlock(Block):
    image = subjunctive.resource.image('images/redblock.png')
    antiblock = "GreenBlock"

if __name__ == '__main__':
    world = Planet()
    cursor = Cursor(world)
    world.setup(cursor)

    def move_cursor(direction):
        cursor.move(direction, orient=True)

    subjunctive.run(world, on_direction=move_cursor)
