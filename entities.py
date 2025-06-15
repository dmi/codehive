class Entity:
    def __init__(self, name, x, y, type="robot", hp=100, strength=10, icon="🤖", state="idle", idle=250, map=None, speed=1.0):
        self.name = name
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.type = type
        self.hp = hp
        self.strength = strength
        self.inventory = []
        self.icon = icon
        self.state = state
        self.idle = idle
        self.cooldown = idle
        self.map = map
        self.speed = speed  # скорость в клетках/секунду
        self.target_x = x
        self.target_y = y
        self.is_moving = False
        self.lerp_factor = 0.0  # 0.0 - начало, 1.0 - конец

    def update(self, dt):
        self.cooldown -= dt
        if self.cooldown <= 0:
            self.cooldown = self.idle
            self.act(dt)

        if self.is_moving:
            self.update_position(dt)

    def update_position(self, dt):
        if self.lerp_factor >= 1.0:
            self.x = self.target_x
            self.y = self.target_y
            self.is_moving = False
            self.lerp_factor = 0.0
            return

        # Линейная интерполяция
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx**2 + dy**2)**0.5
        if distance == 0:
            return

        step = self.speed * dt
        self.lerp_factor += step / distance
        self.lerp_factor = min(1.0, self.lerp_factor)

        self.x += dx * self.lerp_factor
        self.y += dy * self.lerp_factor

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if self.map and self.map.is_bound(new_x, new_y) and self.map.is_walkable(new_x, new_y):
            self.target_x = new_x
            self.target_y = new_y
            self.is_moving = True
            self.state = "moving"
            return True
        self.state = "idle"
        return False

    def act(self, dt):
        pass