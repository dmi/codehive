from entities import Entity
from random import randint

class Builder(Entity):
    def __init__(self, name, x, y, map):
        super().__init__(name, x, y, type="robot", icon="🧱", map=map)

    def act(self, dt):
        dir_x, dir_y = [(-1, 0), (1, 0), (0, -1), (0, 1)][randint(0, 3)]
        if self.map and self.map.is_bound(self.x + dir_x, self.y + dir_y) and not self.map.is_walkable(self.x + dir_x, self.y + dir_y):
            self.dig(dir_x, dir_y)
        elif self.map and self.map.get_tile(self.x, self.y).items:
            self.pick_up()
        else:
            self.move(dir_x, dir_y)