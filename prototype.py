#!python3
# code based off http://www.nandnor.net/?p=64

import pygame
import math
from pygame import *
from entities import *

DISPLAY = (800, 640)
DEPTH = 32
FLAGS = 0

# in blocks, 25 x 20

class Scene(object):
    def __init__(self):
        pygame.init()
        self.screen = display.set_mode(DISPLAY, FLAGS, DEPTH)
        display.set_caption("You are now reading this text")

        self.bg = Surface((32, 32))
        self.bg.convert()
        self.bg.fill(Color("#000000"))

        self.platforms = []
        self.creatures = []
        self.entities = pygame.sprite.Group()

        self.human = None

    def load_level(self, level):
        x = y = 0
        for row in level:
            for col in row:
                if col == "P":
                    platform = Platform(x, y)
                    self.platforms.append(platform)
                    self.entities.add(platform)
                if col == "E":
                    exit = ExitBlock(x, y)
                    self.platforms.append(exit)
                    self.entities.add(exit)
                x += 32
            y += 32
            x = 0

    def clear_level(self):
        self.platforms = []
        self.creatures = []
        self.entities = pygame.sprite.Group()

    def add_creature(self, entity):
        self.entities.add(entity)
        self.creatures.append(entity)

    def enable_human(self):
        if self.human == None:
            self.human = Creature(32, 32, HumanAgent())
            self.add_creature(self.human)

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

            if not self.human is None:
                self.human.agent.set_decision(MoveDecision(left, right, up, down))

            for creature in self.creatures:
                creature.update(self.platforms)
    
            self.draw()

    def draw(self):
        for y in range(20):
            for x in range(25):
                self.screen.blit(self.bg, (x*32, y*32))
        self.entities.draw(self.screen)
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
    s = Swarm(SimpleAgent)
    for guy in s.get_guys():
        scene.add_creature(guy)
    scene.enable_human()
    scene.main_loop()

if(__name__ == "__main__"):
    main()
