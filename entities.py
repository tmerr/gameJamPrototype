#!python3

import pygame
import math
from pygame import *
from agents import *
from bodies import *

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Creature(Entity):
    def __init__(self, x, y, agent, body, surface, rect = None):
        Entity.__init__(self)
        self.agent = agent
        self.image = surface
        if rect is None:
            self.rect = Rect(x, y, surface.get_width(), surface.get_height())
        else:
            self.rect = rect

        self.body = body
        self.body.set_rect(self.rect)

    def update(self, platforms):
        decision = self.agent.decide_move(self.body, platforms)
        self.body.act(decision, platforms)

class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)
    
    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))
