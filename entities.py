#!python3

import pygame
import math
from pygame import *
from agents import *

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Creature(Entity):
    def __init__(self, x, y, agent, surface, rect = None):
        Entity.__init__(self)
        self.agent = agent
        self.xvel = 0
        self.yvel = 0
        self.on_ground = False
        self.image = surface
        if rect is None:
            self.rect = Rect(x, y, surface.get_width(), surface.get_height())
        else:
            self.rect = rect

    def update(self, platforms):
        decision = self.agent.decide_move(self, platforms)
        if decision.up and self.on_ground:
            self.yvel -= 7
        if decision.down:
            pass
        self.xvel = 0
        if decision.left:
            self.xvel -= 5
        if decision.right:
            self.xvel += 5

        if (not self.on_ground) and self.yvel <= 30:
            self.yvel += 0.3
        if not (decision.left or decision.right):
            self.xvel = 0
        self.rect.left += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.rect.top += self.yvel
        self.on_ground = False
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for platform in platforms:
            if sprite.collide_rect(self, platform):
                if isinstance(platform, ExitBlock):
                    event.post(event.Event(QUIT))
                if xvel > 0: self.rect.right = platform.rect.left
                if xvel < 0: self.rect.left = platform.rect.right
                if yvel > 0:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = platform.rect.bottom
                    self.yvel = -self.yvel*(2/3)

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
