from pygame import *
from collections import namedtuple
import random

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

