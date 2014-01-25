#!python3

import pygame
import math
from pygame import *
from collections import namedtuple
import random

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

MoveDecision = namedtuple("MoveDecision", "left right up down")

class RandomAgent(object):
    """Agent that jitters around randomly"""
    def decide_move(self, player, platforms):
        return MoveDecision(*[random.choice((False, True)) for i in range(4)])

class SimpleAgent(object):
    """Agent that jumps over every wall it hits, and if it fails reverses directions"""
    def __init__(self):
        self.must_jump = True
        self.right = True # or left
        self.halt = False

    def decide_move(self, player, platforms):
        # Extract data from player object
        x, y = player.rect.x, player.rect.y
        on_ground = player.on_ground

        # Randomize how far away from a block before jump
        howfar = random.randint(1, 64) 
        up = False
        # Make pretend sprites to check for collisions to the left and right
        left_shift = type('obj', (object,), {'rect': Rect(x - howfar, y, 32, 32)})
        right_shift = type('obj', (object,), {'rect': Rect(x + howfar, y, 32, 32)})
        # Jump something's in the way
        if on_ground:
            self.halt = False
            # Check collision right side
            if not self.right and sprite.spritecollideany(left_shift, platforms):
                if self.must_jump:
                    up = True
                    self.halt = False
                    self.must_jump = False
                else:
                    self.right = True
                    self.must_jump = True
            # Check collision left side
            elif self.right and sprite.spritecollideany(right_shift, platforms):
                if self.must_jump:
                    up = True
                    self.halt = False
                    self.must_jump = False
                else:
                    self.right = False
                    self.must_jump = True
            else:
                self.must_jump = True
        else:
            # Randomly stop moving forward in air, so we don't skip over stepping stones
            if random.random() < 1./20:
                self.halt = True

        return MoveDecision(not self.right and not self.halt, self.right and not self.halt, up, False)

class HumanAgent(object):
    """Agent that should be manually set from the outside"""
    def __init__(self):
        self.move_decision = MoveDecision(False, False, False, False)

    def set_decision(self, move_decision):
        self.move_decision = move_decision

    def decide_move(self, player, platforms):
        return self.move_decision

class Player(Entity):
    def __init__(self, x, y, agent):
        Entity.__init__(self)
        self.agent = agent
        self.xvel = 0
        self.yvel = 0
        self.on_ground = False
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#FF0000"))
        self.rect = Rect(x, y, 32, 32)

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

class Swarm(object):
    def __init__(self, AgentType):
        self.guys = []
        for y in range(32, 320, 64):
            self.guys.append(Player(32, y, AgentType()))

    def update(self, platforms):
        for guy in self.guys:
            guy.update(platforms)

    def get_guys(self):
        return self.guys

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
