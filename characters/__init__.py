from .robot import Robot
from .builder import Builder
from .ghost import Ghost
from .cursor import Cursor

from random import randint

# Животные: 🐶 🐱 🦁  
# Монстры: 👻 🧟‍♂️ 👾  
# Растения: 🌿 🌱 🌳
# Инструменты: 🔧 🛠️ 🪓 🧰 🧯 🔨 ⛏️
# Дверь: 🚪
# Стена 🧱
# Не знаю что: 🛷 🚬

def get_all_characters(map):

    robots = [ Robot(name=f'Rx{randint(0,1023)}-{randint(0,64)}', x=randint(0, map.width-1), y=randint(0, map.height-1), map=map)
               for r in range(100)
             ]
    
    ghosts = [ Ghost(name=f'G-{randint(0,1023)}-{randint(0,64)}', x=randint(0, map.width-1), y=randint(0, map.height-1), map=map)
               for r in range(100)
             ]
    cursor = Cursor(x=map.width//2, y=map.height//2, map=map)
    return [cursor] + robots + ghosts