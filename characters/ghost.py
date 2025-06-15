from entities import Entity
from random import randint

class Ghost(Entity):
    def __init__(self, name, x, y, map):
        super().__init__(name, x, y, type="robot", icon="👻", map=map)

    def act(self, dt):
        dir_x, dir_y = [(-1, 0), (1, 0), (0, -1), (0, 1)][randint(0, 3)]
        self.move(dir_x, dir_y)