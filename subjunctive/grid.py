import sdl2

class Direction:
    def __init__(self, name, value, number_of_directions):
        self._number_of_directions = number_of_directions
        self.name = name
        self._value = value

    def __str__(self):
        return "<Direction %r>" % self.name

    def __sub__(self, other):
        "Return the number of clockwise 90° rotations between self and other"
        return (self._value - other._value) % self._number_of_directions

class Grid:
    def __init__(self, width, height, offset_x=None, offset_y=None):
        self.width = width
        self.height = height
        self.Location = _make_location_class(self, (width, height))

class OutOfBounds(Exception):
    pass

def _make_location_class(parent, grid_size):
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
            if direction == left:
                return self.__class__(self.x - 1, self.y)
            elif direction == down:
                return self.__class__(self.x, self.y + 1)
            elif direction == up:
                return self.__class__(self.x, self.y - 1)
            elif direction == right:
                return self.__class__(self.x + 1, self.y)
            else:
                raise ValueError("Invalid direction: {}".format(direction_))

    Location.__qualname__ = parent.__class__.__qualname__ + ".Location"
    return Location

left = Direction('left', 0, 4)
up = Direction('up', 1, 4)
right = Direction('right', 2, 4)
down = Direction('down', 3, 4)

KEYBOARD = {sdl2.SDLK_LEFT: left,
            sdl2.SDLK_UP: up,
            sdl2.SDLK_RIGHT: right,
            sdl2.SDLK_DOWN: down}
