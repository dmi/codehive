from .robot import Robot
from .builder import Builder
from .ghost import Ghost
from random import randint

def get_all_characters(map):

    robots = [ Robot(name=f'Rx{randint(0,1023)}-{randint(0,64)}', x=randint(0, map.width-1), y=randint(0, map.height-1), map=map)
               for r in range(100)
             ]
    
    ghosts = [ Ghost(name=f'G-{randint(0,1023)}-{randint(0,64)}', x=randint(0, map.width-1), y=randint(0, map.height-1), map=map)
               for r in range(100)
             ]
    return robots + ghosts