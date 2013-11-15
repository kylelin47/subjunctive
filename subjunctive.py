import logging
import random
import sys

import pyglet
import pyglet.gl as gl

KEYBOARD_DIRECTIONS = {pyglet.window.key.MOTION_LEFT: 'left',
                       pyglet.window.key.MOTION_DOWN: 'down',
                       pyglet.window.key.MOTION_UP: 'up',
                       pyglet.window.key.MOTION_RIGHT: 'right'}

class God:
    __slots__ = []
God = God()

class OutOfBounds(Exception):
    pass

def make_location_class(grid_size):
    """Make a specialized Location class that validates its input

    Instances of the returned class will raise an exception if they are
    constructed with values that are out-of-bounds.

    """
    class Location:
        __slots__ = ['__x', '__y']
        max = grid_size

        def __eq__(self, other):
            return self.x == other.x and self.y == other.y

        def __hash__(self):
            return hash((self.x, self.y))

        def __init__(self, x, y):
            if not (isinstance(x, int) and isinstance(y, int)):
                raise TypeError("Location object needs integers")
            if not 0 <= x < self.max[0] or not 0 <= y < self.max[1]:
                raise OutOfBounds
            self.__x = x
            self.__y = y

        def __repr__(self):
            return "Location({}, {})".format(self.x, self.y)

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        def adjacent(self, direction):
            if direction == 'left':
                return self.__class__(self.x - 1, self.y)
            elif direction == 'down':
                return self.__class__(self.x, self.y - 1)
            elif direction == 'up':
                return self.__class__(self.x, self.y + 1)
            elif direction == 'right':
                return self.__class__(self.x + 1, self.y)
            else:
                raise ValueError("Invalid direction: {}".format(direction))

    return Location

class World(pyglet.window.Window):
    background = None
    grid_offset = (0, 0)
    grid_size = (8, 8)
    score_offset = None
    tile_size = (16, 16)
    window_caption = "Subjunctive!"

    @property
    def center(self):
        return self.Location(self.grid_size[0] // 2, self.grid_size[1] // 2)

    def __init__(self):
        if self.background is not None:
            width = self.background.width
            height = self.background.height
        else:
            width = self.grid_size[0] * self.tile_size[0]
            height = self.grid_size[1] * self.tile_size[1]
        super().__init__(width=width, height=height,
                         caption=self.window_caption)

        # Enable rendering with transparency
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # Create a grid-aware Location class
        self.Location = make_location_class(self.grid_size)
        self.Location.__qualname__ = self.__class__.__qualname__ + ".Location"

        # Create a batch to draw the sprites
        self.batch = pyglet.graphics.Batch()

        # Set up locations
        self._entities = {self.Location(x, y): None
                          for x in range(self.grid_size[0])
                          for y in range(self.grid_size[1])}

        self.score = 0
        if self.score_offset:
            # Create a score label
            x, y = self.score_offset
            self.score_label = pyglet.text.Label(
                "", bold=True, color=(0, 0, 0, 255), x=x, y=y)

    def clear(self):
        self._entities = {self.Location(x, y): None
                          for x in range(self.grid_size[0])
                          for y in range(self.grid_size[1])}

    def count(self, entity_type):
        return sum(1 for e in self._entities.values()
                   if isinstance(e, entity_type))

    @classmethod
    def load(cls, level_file, definitions_file):
        # TODO: Load definitions from the file
        types = {'-': None, 'a': Entity}

        with open(level_file) as f:
            lines = [line for line in map(str.strip, f) if line != '']

        width, height = len(lines[0]), len(lines)
        world = cls()
        world.grid_size = width, height

        for ny, line in enumerate(lines, start=1):
            y = height - ny
            for x, char in enumerate(line):
                try:
                    entity_type = types[char]
                except KeyError:
                    logging.error("Character {!r} is not defined; ignoring"
                                  "".format(char))
                else:
                    if entity_type:
                        world.place(entity_type(), world.Location(x, y))

        return world

    def locate(self, entity):
        for location, suspect in self._entities.items():
            if suspect is entity:
                return location
        raise ValueError("{} not in world".format(entity))

    def on_draw(self):
        # Update the position of each sprite
        for location, entity in self._entities.items():
            if entity:
                s = entity.sprite
                x, y = self._pixels(location)
                if s.rotation == 90:
                    y += s.image.height
                elif s.rotation == 180:
                    x += s.image.width
                    y += s.image.height
                elif s.rotation == 270:
                    x += s.image.width
                s.set_position(x, y)
        if self.background:
            self.background.blit(0, 0)
        self.batch.draw()

        # Draw the score
        if self.score_offset:
            self.score_label.text = str(self.score)
            self.score_label.draw()

    def _pixels(self, location):
        return (location.x * self.tile_size[0] + self.grid_offset[0],
                location.y * self.tile_size[1] + self.grid_offset[1])

    def place(self, entity, location):
        logging.debug("Placing {} at {}".format(entity, location))
        if self._entities[location] is not None:
            raise ValueError("Location {} already contains {}"
                             "".format(location, self._entities[location]))
        self._entities[location] = entity

    def push(self, entity, direction, pusher=God):
        if pusher is God:
            entity.direction = direction


        action = entity.respond_to_push(direction, pusher, self)
        if action == "move":
            try:
                new_location = self.locate(entity).adjacent(direction)
            except OutOfBounds:
                return "stay"

            if self._entities[new_location]:
                neighbor_action = self.push(self._entities[new_location],
                                            direction, entity)
                if neighbor_action == "move":
                    logging.debug("{} is moving (neighbor)".format(entity))
                    self.remove(entity)
                    self.place(entity, new_location)
                    return "move"
                elif neighbor_action == "consume":
                    logging.debug("{} is being consumed".format(entity))
                    self.remove(entity)
                    return "move"
                elif neighbor_action == "stay":
                    logging.debug("{} is staying".format(entity))
                    return "stay"
                else:
                    logging.debug("{} is doing {} (neighbor)".format(entity, action))
                    return neighbor_action
            else:
                logging.debug("{} is moving (no neighbor)".format(entity))
                self.remove(entity)
                self.place(entity, new_location)
                return "move"
        elif action == "vanish":
            logging.debug("{} is vanishing".format(entity))
            self.remove(entity)
            return "move"
        elif action == "mad":
            logging.debug("{} is madding".format(entity))
            self.remove(entity)
            return "consume"
        else:
            logging.debug("{} is doing {}".format(entity, action))
            return action

    def read_level(self, path):
        columns = []
        with open(path, "r") as leveltext_file:
            rows = leveltext_file.read().splitlines()
            for i in rows:
                columns.append(i.split())
        return rows, columns

    def remove(self, entity):
        location = self.locate(entity)
        self._entities[location] = None
        return location

    def replace(self, entity, new_entity):
        location = self.remove(entity)
        self.place(new_entity, location)

    def place_objects(self, obj_list, rows, columns):
        for ly, i in enumerate(rows):
            for lx, j in enumerate(columns[ly]):
                try:
                    e = obj_list[j]()
                    self.place(e, self.Location(lx,self.grid_size[1]-ly-1))
                except KeyError:
                    pass

    def spawn_random(self, entity_type, number=1, cursor=None):
        logging.debug("Spawning {} {}s".format(number, entity_type))
        new_entities = []
        for _ in range(number):
            # TODO: Don't use locations that are in the same row or column as
            # the cursor if a cursor is passed.
            if cursor is None:
                available_locations = [location for location, entity
                                       in self._entities.items() if not entity]
            else:
                available_locations = []
                cursor_location = self.locate(cursor)
                x_max, y_max = self.grid_size
                invalid_xloc = [cursor_location.x, 0, x_max - 1]
                invalid_yloc = [cursor_location.y, 0, y_max - 1]
                for location, entity in self._entities.items():
                    if not entity:
                        _x, _y = location.x, location.y
                        if not _x in invalid_xloc and not _y in invalid_yloc:
                            available_locations.append(location)
            if not available_locations:
                break
            location = random.choice(available_locations)
            e = entity_type(self)
            self.place(e, location)
            new_entities.append(e)
        return new_entities

class Entity:
    directional = False
    pushable = False

    def __init__(self, world, *, direction='right', name=None):
        # Create the sprite first to avoid problems with overridden setters
        # that try to access the sprite
        self.sprite = pyglet.sprite.Sprite(self.image, batch=world.batch)
        self.direction = direction
        self.name = self.__class__.__name__ if name is None else name
        self.world = world

    def __str__(self):
        return self.name

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction
        if self.directional:
            rotate(self.sprite, direction)

    @property
    def image(self):
        return pyglet.resource.image('images/default.png')

    @image.setter
    def image(self, image):
        self.sprite.image = image

    def respond_to_push(self, direction, pusher, world):
        """Called to determine what should happen when the entity is pushed

        Possible return values: "stay", "move", "vanish", "consume", "mad"
        """
        return "move" if self.pushable else "stay"

def rotate(sprite, direction):
    rotation = {'left': 180, 'down': 90, 'up': 270, 'right': 0}
    sprite.rotation = rotation[direction]


if '--debug' in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

pyglet.resource.path.append('@subjunctive')
pyglet.resource.reindex()
