from entities import Entity
from emojis import get_emoji

class Cursor(Entity):
    def __init__(self, x, y, map):
        super().__init__(
            name="Курсор",
            x=x,
            y=y,
            type="cursor",
            icon="+",
            state="idle",
            map=map
        )

    def act(self, dt):
        if self.ctl_dx or self.ctl_dy:
            self.move(self.ctl_dx, self.ctl_dy)