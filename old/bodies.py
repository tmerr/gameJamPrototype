from pygame import *
import entities
import pygame
import math

class Body(object):
    def set_rect(self, rect):
        pass

    def act(self, decision, platforms):
        pass

    def collide(self, xvel, yvel, rect, platforms):
        for platform in platforms:
            if sprite.collide_rect(self, platform):
                if isinstance(platform, entities.ExitBlock):
                    event.post(event.Event(QUIT))
                if xvel > 0: rect.right = platform.rect.left
                if xvel < 0: rect.left = platform.rect.right
                if yvel > 0:
                    rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.yvel = 0
                if yvel < 0:
                    rect.top = platform.rect.bottom
                    self.yvel = -self.yvel * self.head_bounce

class JumperBody(Body):
    def __init__(self):
        self.jump_velocity = 7
        self.gravity = 0.3
        self.max_fall = 30
        self.move_velocity = 5
        self.head_bounce = 2/3
        
        self.rect = None
        self.xvel = 0
        self.yvel = 0
        self.on_ground = False

    def set_rect(self, rect):
        self.rect = rect

    def act(self, decision, platforms):
        assert not self.rect is None

        if decision.up and self.on_ground:
            self.yvel -= self.jump_velocity
        if decision.down:
            pass
        self.xvel = 0
        if decision.left:
            self.xvel -= self.move_velocity
        if decision.right:
            self.xvel += self.move_velocity

        if (not self.on_ground) and self.yvel <= self.max_fall:
            self.yvel += self.gravity
        if not (decision.left or decision.right):
            self.xvel = 0
        self.rect.left += self.xvel
        self.collide(self.xvel, 0, self.rect, platforms)
        self.rect.top += self.yvel
        self.on_ground = False
        self.collide(0, self.yvel, self.rect, platforms)

class WalkerBody(Body):
    def __init__(self):
        self.jump_velocity = 7
        self.gravity = 0.3
        self.max_fall = 30
        self.move_velocity = 5
        self.head_bounce = 2/3

        self.rect = None
        self.xvel = 0
        self.yvel = 0
        self.on_ground = False

    def set_rect(self, rect):
        self.rect = rect

    def act(self, decision, platforms):
        assert not self.rect is None

        if decision.down or decision.up:
            pass
        self.xvel = 0
        if decision.left:
            self.xvel -= self.move_velocity
        if decision.right:
            self.xvel += self.move_velocity

        if (not self.on_ground) and self.yvel <= self.max_fall:
            self.yvel += self.gravity
        if not (decision.left or decision.right):
            self.xvel = 0
        self.rect.left += self.xvel
        self.collide(self.xvel, 0, self.rect, platforms)
        self.rect.top += self.yvel
        self.on_ground = False
        self.collide(0, self.yvel, self.rect, platforms)


