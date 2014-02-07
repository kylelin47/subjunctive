from . import grid
from . import resource

class Entity:
    orientable = False
    image = resource.image('images/default.png')
    pushable = False

    def __init__(self, world, *, direction=grid.up, name=None):
        self.direction = direction
        self.name = self.__class__.__name__ if name is None else name
        self.world = world

    def __str__(self):
        return self.name

    def move(self, direction, *, orient=False):
        if orient:
            self.direction = direction
        try:
            new_location = self.world.locate(self).adjacent(direction)
        except grid.OutOfBounds:
            return
        blocking_entity = self.world._entities.get(new_location)
        if blocking_entity:
            blocking_entity.push(direction, self)
        if not self.world._entities[new_location]:
            try:
                self.world.remove(self)
            except ValueError:
                # This means someone else removed us, so give up
                return
            else:
                self.world.place(self, new_location)

    def push(self, direction, pusher=None):
        """Return what should happen when the entity is pushed

        Entities can override this method to get special behavior.
        """
        if self.pushable:
            self.move(direction, orient=self.orientable)
