from pygame import *
from entities import *
import actions

class Brain(object):
    def choose_action(self, metrics, stats, platforms):
        pass

class PooBrain(Brain):
    def __init__(self):
        self.moving_right = True # or left

    def choose_action(self, metrics, stats, platforms):
        howfar = 1
        x, y = metrics.rect.x, metrics.rect.y
        left_shift = type('obj', (object,), {'rect': Rect(x - howfar, y, 32, 32)})
        right_shift = type('obj', (object,), {'rect': Rect(x + howfar, y, 32, 32)})
        if not self.moving_right and pygame.sprite.spritecollideany(left_shift, platforms):
            self.moving_right = True
        if self.moving_right and pygame.sprite.spritecollideany(right_shift, platforms):
            self.moving_right = False
        
        if self.moving_right:
            return actions.move_right
        else:
            return actions.move_left
