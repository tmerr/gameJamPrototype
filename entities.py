import pygame
import math
from pygame import *

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#FF0000"))
        self.rect = Rect(x, y, 32, 32)
    
    def update(self, up, down, left, right, platforms):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 7
        if down:
            pass
        if left:
            self.xvel = -5
        if right:
            self.xvel = 5
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 30: self.yvel = 30
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)
    
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    event.post(event.Event(QUIT))
                if xvel > 0: self.rect.right = p.rect.left
                if xvel < 0: self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0: self.rect.top = p.rect.bottom

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


class Swarm(Entity):
    def __init__(self):
        self.guys = []
        #self.guys.append()

    def update(self, platforms):
        pass

    def get_guys(self):
        return self.guys

class Guy(Entity):
    def __init__(self, x, y):
        pass
