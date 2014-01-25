import random
from pygame import *

def solid(color, w=32, h=32):
    """takes a pygame color ex Color('#FF0000')"""
    surface = Surface((w, h))
    surface.convert()
    surface.fill(color)
    return surface

def random_solid(w=32, h=32):
    r = lambda: random.randint(0,255)
    color = Color(r(), r(), r())
    return solid(color, w, h)
