from .robot import Robot
from .builder import Builder

def get_all_characters(map):
    return [
        Robot(name="Робот", x=50, y=50, map=map),
        Builder(name="Строитель", x=56, y=55, map=map),
    ]