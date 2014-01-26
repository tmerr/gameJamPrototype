import entities
from pygame import *
from collections import namedtuple

def check_collisions(metrics, world):
    """Return platform colliding with or None"""    
    otherplat = sprite.spritecollideany(metrics, world.platforms)
    othersprite = None
    for creature in world.creatures:
        if creature.metrics != metrics and sprite.collide_rect(metrics, creature):
            othersprite = sprite.spritecollideany(metrics, world.creatures)
    
    other = otherplat or othersprite
    if other is None:
        return None
    else:
        overlap_left = metrics.rect.left < other.rect.right
        overlap_right = metrics.rect.right > other.rect.left
        overlap_top = metrics.rect.top < other.rect.bottom
        overlap_bottom = metrics.rect.bottom > other.rect.top
        
        Overlaps = namedtuple('Overlaps', 'left right top bottom')
        overlaps = Overlaps(overlap_left, overlap_right, overlap_top, overlap_bottom)
        Collision = namedtuple('Collision', 'other overlaps')
        return Collision(other, overlaps)


def move_right(metrics, stats, world):
    metrics.rect.x += 7
    
    collision = check_collisions(metrics, world)
    if collision and collision.overlaps.right:
        #metrics.rect.right = collision.other.rect.left
        metrics.rect.x -= 7

def move_left(metrics, stats, world):
    metrics.rect.x -= 7
    collision = check_collisions(metrics, world)
    if collision and collision.overlaps.left:
        #metrics.rect.left = collision.other.rect.right
        metrics.rect.x += 7

def jump(metrics, stats, world):
    pass

def gravity(metrics, stats, world):
    metrics.rect.y += metrics.yvel
    
    collision = check_collisions(metrics, world)
    if collision and collision.overlaps.bottom:
        metrics.yvel = 0
        metrics.rect.bottom = collision.other.rect.top
    elif metrics.yvel <= 30:
        metrics.yvel += 0.3