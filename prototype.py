#!python3
# code based off http://www.nandnor.net/?p=64

import pygame
import math
from pygame import *
from entities import *
from brain import *
import surfaces

DISPLAY = (800, 640)
DEPTH = 32
FLAGS = 0

class World(object):
    """A container for the entities in the world"""
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.creatures = pygame.sprite.Group()
    
# in blocks, 25 x 20

class Scene(object):
    def __init__(self):
        pygame.init()
        self.screen = display.set_mode(DISPLAY, FLAGS, DEPTH)
        display.set_caption("You are now reading this text")

        self.bg = Surface((32, 32))
        self.bg.convert()
        self.bg.fill(Color("#000000"))

        self.level_width = None
        self.level_height = None
        self.world = World()

    def load_level(self, level):
        self.level_width = len(level[0])
        self.level_height = len(level)
        x = y = 0
        for row in level:
            assert len(row) == self.level_width
            for col in row:
                if col == "P":
                    platform = Platform(x, y)
                    self.world.platforms.add(platform)
                if col == "E":
                    exit = ExitBlock(x, y)
                    self.world.platforms.add(exit)
                x += 32
            y += 32
            x = 0

    def clear_level(self):
        self.level_width = None
        self.level_height = None
        self.world.platforms.empty()
        self.world.creatures.empty()

    def add_creature(self, entity):
        self.world.creatures.add(entity)

    def main_loop(self):
        timer = time.Clock()
        up = down = left = right = False
        while 1:
            timer.tick(60)
            for e in pygame.event.get():
                if e.type == QUIT:
                    raise(SystemExit)
                if e.type == KEYDOWN and e.key == K_ESCAPE: 
                    raise(SystemExit)
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYDOWN and e.key == K_q:
                    metrics = Metrics(Rect(32, 32, 32, 32), 0, 0)
                    stats = Metrics(None, None, None)
                    c = Creature(metrics, stats, PooBrain(), surfaces.random_solid())
                    self.add_creature(c)
                if e.type == KEYDOWN and e.key == K_w:
                    pass
                if e.type == KEYDOWN and e.key == K_DOWN:
                    down = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                
                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYUP and e.key == K_DOWN:
                    down = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False

            self.world.platforms.update()
            self.world.creatures.update(self.world)
    
            self.draw()

    def draw(self):
        for y in range(self.level_height):
            for x in range(self.level_width):
                self.screen.blit(self.bg, (x*32, y*32))
        self.world.platforms.draw(self.screen)
        self.world.creatures.draw(self.screen)
        pygame.display.flip()

def main():
    scene = Scene()
    scene.load_level([
        "PPPPPPPPPPPPPPPPPPPPPPPPP",
        "P  P                    P",
        "P  PPPPPP               P",
        "P  P     P    P         P",
        "P  P      P   P         P",
        "P  P       P  P         P",
        "P  P         PP    PPPPPP",
        "P  P        P P         P",
        "P  P       P  P         P",
        "P  P      P   PPPPPP    P",
        "P  P     P    PP        P",
        "P  P PP       PPP      PP",
        "P  PPPPP      PPPP    PPP",
        "P       P     PPPPP  PPPP",
        "P        PP   P         P",
        "P            PP         P",
        "P          PP P         P",
        "P       PP    P         P",
        "P      PPPP   PE        P",
        "PPPPPPPPPPPPPPPPPPPPPPPPP",
    ])
    #scene.enable_human()
    scene.main_loop()

if(__name__ == "__main__"):
    main()
