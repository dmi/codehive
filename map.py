import random

class Tile:
    def __init__(self, is_walkable=True, material=None, hardness=0, items=None):
        self.is_walkable = is_walkable
        self.material = material  # "stone", "wood", "dirt"
        self.hardness = hardness  # твёрдость (кол-во попыток разрушить)
        self.items = items or []

    def get_color(self):
        if not self.is_walkable:
            if self.material == "stone":
                return (100, 100, 100)
            elif self.material == "wood":
                return (139, 69, 19)
            elif self.material == "dirt":
                return (150, 75, 0)
        return (255, 255, 255)  # Пустая клетка

class Map:
    def __init__(self, width=100, height=100, TILE_SIZE=32):
        self.width = width
        self.height = height
        self.TILE_SIZE = TILE_SIZE
        self.tiles = [[Tile() for _ in range(width)] for _ in range(height)]

        # Генерация препятствий
        for y in range(height):
            for x in range(width):
                if random.random() < 0.2:
                    material = random.choice(["stone", "wood", "dirt"])
                    hardness = 3 if material == "stone" else 2 if material == "wood" else 1
                    self.tiles[y][x] = Tile(is_walkable=False, material=material, hardness=hardness)

    def is_bound(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and self.tiles[y][x].is_walkable

    def get_tile(self, x, y):
        return self.tiles[y][x]
    
    def look_up(self, entity):
        tile = self.get_tile(entity.x, entity.y)
        return tile.items
    
    def pick_up(self, entity, items):
        tile = self.get_tile(entity.x, entity.y)
        itms = tile.items.copy()
        tile.items = []
        return itms
    
    def dig(self, entity):
        if self.is_bound(entity.x + entity.dx, entity.y + entity.dy):
            tile = entity.map.get_tile(entity.x + entity.dx, entity.y + entity.dy)
            if not tile.is_walkable and tile.hardness > 0:
                tile.hardness -= 1
                if tile.hardness == 0:
                    tile.is_walkable = True
                    tile.material = None
            return tile.material, tile.hardness
        else:
            return None, None