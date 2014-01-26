#!python3

import pygame
import math
from pygame import *
from collections import namedtuple
import actions

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Metrics(object):
    def __init__(self, rect, xvel, yvel):
        self.rect = rect
        self.xvel = xvel
        self.yvel = yvel

class Stats(object):
    def __init__(self, weight, jump_velocity, odor):
        self.weight = weight
        self.jump_velocity = jump_velocity
        self.odor = odor

class Creature(Entity):
    def __init__(self, metrics, stats, brain, surface):
        Entity.__init__(self)
        self.metrics = metrics
        self.stats = stats
        self.brain = brain
        self.image = surface
        self.rect = metrics.rect

        # Default rect value?
        # self.rect = Rect(x, y, surface.get_width(), surface.get_height())

    def update(self, world):
        action = self.brain.choose_action(self.metrics, self.stats, world)
        action(self.metrics, self.stats, world)
        actions.gravity(self.metrics, self.stats, world)

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
