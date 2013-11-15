import pyglet

import subjunctive

class Planet(subjunctive.World):
    background = pyglet.resource.image('images/whiteplane.png')
    grid_offset = (0, 0)
    grid_size = (12, 12)
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

class Block(subjunctive.Entity):
    image = pyglet.resource.image('images/defaultblock.png')
    pushable = True
    antiblock = None

    def respond_to_push(self, direction, pusher, world):
        if pusher.__class__.__name__ == self.antiblock:
            return "mad"
        if isinstance(pusher, Cursor) or pusher.__class__ == self.__class__:
            return "move"
        return "stay"

class BlueBlock(Block):
    image = pyglet.resource.image('images/blueblock.png')
    antiblock = "OrangeBlock"

class Cursor(subjunctive.Entity):
    directional = True
    image = pyglet.resource.image('images/cursor.png')
    pushable = True

class GreenBlock(Block):
    image = pyglet.resource.image('images/greenblock.png')
    antiblock = "RedBlock"

class OrangeBlock(Block):
    image = pyglet.resource.image('images/orangeblock.png')
    antiblock = "BlueBlock"

class RedBlock(Block):
    image = pyglet.resource.image('images/redblock.png')
    antiblock = "GreenBlock"

if __name__ == '__main__':
    world = Planet()
    cursor = Cursor(world)
    world.setup(cursor)

    @world.event
    def on_text_motion(motion):
        direction = subjunctive.KEYBOARD_DIRECTIONS.get(motion, False)
        if direction:
            world.push(cursor, direction)
    pyglet.app.run()
