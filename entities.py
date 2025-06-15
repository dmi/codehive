class Entity:
    def __init__(self, name, x, y, type="robot", hp=100, strength=10, icon="🤖", state="idle", idle=250, map=None):
        self.name = name
        self.x = x
        self.y = y
        self.dx = 0 # направление
        self.dy = 0 # направление
        self.type = type
        self.hp = hp
        self.strength = strength
        self.inventory = []
        self.icon = icon  # Теперь это эмодзи
        self.state = state
        self.idle = idle
        self.cooldown = idle  # время до следующего действия
        self.map = map  # Теперь инициализируется при создании

    def update(self, dt):
        self.cooldown -= dt
        if self.cooldown <= 0:
            self.cooldown = self.idle
            self.act(dt)

    def act(self, dt):
        pass

    def move(self, dx, dy):
        self.dx = dx
        self.dy = dy
        new_x = self.x + dx
        new_y = self.y + dy
        if self.map.is_walkable(new_x, new_y):
            self.x, self.y = new_x, new_y
            self.state = "moving"
            return True
        self.state = "idle"
        return False

    def attack(self, target):
        target.hp -= self.strength
        self.state = "attacking"
        print(f"{self.name} атаковал {target.name}, осталось {target.hp} HP")

    def pick_up(self):
        itms = self.map.look_up(self)
        self.inventory.extend(self.map.pick_up(self, itms))
        self.state = "picking_up"
        print(f"{self.name} подобрал {item.name}")

    def dig(self, dx, dy):
        self.dx = dx
        self.dy = dy
        if self.map.is_bound(self.x + dx, self.y + dy) and not self.map.is_walkable(self.x + dx, self.y + dy):
            material, hardness = self.map.dig(self)
            print(f"{self.name} копает {material}, осталось {hardness} попыток")
            self.state = "digging"
        else:
            print(f"{self.name} копает вникуда")
            self.state = "idle"