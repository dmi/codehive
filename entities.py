from logger import record
from emojis import get_emoji

def sign(x):
    return (x > 0) - (x < 0)

class Entity:
    def __init__(self, name, x, y, type="robot", hp=100, strength=10, icon="🤖", state="idle", idle=250, map=None):
        self.name = name
        self.x = x
        self.y = y
        self.dx = 0  # направление по x
        self.dy = 0  # направление по y
        self.ctl_dx = 0 # управление по x
        self.ctl_dy = 0 # управление по у
        self.type = type
        self.hp = hp
        self.strength = strength
        self.inventory = []
        self.icon = icon  # Теперь это эмодзи
        self.state = state
        self.idle = idle  # время между действиями
        self.cooldown = idle  # время до следующего действия
        self.map = map  # Теперь инициализируется при создании
        self.vx = 0  # смещение по x
        self.vy = 0  # смещение по y
        self.emoji = get_emoji(icon, (self.map.TILE_SIZE, self.map.TILE_SIZE))

    def update(self, dt, visible=True):
        self.cooldown -= dt
        if self.cooldown <= 0:
            self.cooldown = self.idle  # время до следующего действия
            self.act(dt)

        if visible:
            # Плавное перемещение
            if self.state == "moving":
                # Скорость перемещения (в пикселях за миллисекунду)
                speed = self.map.TILE_SIZE / self.idle
                # Смещение за этот кадр
                move_x = speed * dt * self.dx
                move_y = speed * dt * self.dy
                
                # Обновление смещения
                self.vx += move_x
                self.vy += move_y
                
                # Проверка и сброс смещения при достижении целевой клетки
                if sign(self.vx) == sign(self.dx): #>= self.map.TILE_SIZE:
                    self.vx = 0
                if sign(self.vy) == sign(self.dy): #>= self.map.TILE_SIZE:
                    self.vy = 0
                if self.vx == 0 and self.vy == 0:
                    self.state = "idle"
            elif self.state == "idle":
                pass

    def act(self, dt):
        pass

    def move(self, dx, dy):
        self.dx = dx
        self.dy = dy
        new_x = self.x + dx
        new_y = self.y + dy
        if self.type=="cursor" and self.map.is_bound(new_x, new_y) or self.map.is_walkable(new_x, new_y):
            self.x, self.y = new_x, new_y
            self.vx = -dx * self.map.TILE_SIZE
            self.vy = -dy * self.map.TILE_SIZE
            self.state = "moving"
            return True
        self.state = "idle"
        return False

    def attack(self, target):
        target.hp -= self.strength
        self.state = "attacking"
        record(f"{self.name} атаковал {target.name}, осталось {target.hp} HP", self.name)

    def pick_up(self):
        itms = self.map.look_up(self)
        self.inventory.extend(self.map.pick_up(self, itms))
        self.state = "picking_up"
        record(f"{self.name} подобрал {[i.name for i in itms]}", self.name)

    def dig(self, dx, dy):
        self.dx = dx
        self.dy = dy
        if self.map.is_bound(self.x + dx, self.y + dy) and not self.map.is_walkable(self.x + dx, self.y + dy):
            material, hardness = self.map.dig(self)
            record(f"{self.name} копает {material}, осталось {hardness} попыток", self.name)
            self.state = "digging"
        else:
            record(f"{self.name} копает вникуда", self.name)
            self.state = "idle"