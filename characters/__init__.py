from .robot import Robot
from .builder import Builder

def get_all_characters(map):
    return [
        Robot(name="Робот", x=5, y=5, map=map),
        Builder(name="Строитель", x=6, y=5, map=map),
    ]