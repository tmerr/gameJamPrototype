import entities
from pygame import *

def check_collisions(metrics, platforms):
    """Return platform colliding with or None"""
    for platform in platforms:
        if sprite.collide_rect(metrics, platform):
            return platform

def move_right(metrics, stats, platforms):
    metrics.rect.x += 7
    other = check_collisions(metrics, platforms)
    if not other is None:
        metrics.rect.right = other.rect.left

def move_left(metrics, stats, platforms):
    metrics.rect.x -= 7
    other = check_collisions(metrics, platforms)
    if not other is None:
        metrics.rect.left = other.rect.right

def jump(metrics, stats, platforms):
    pass

def gravity(metrics, stats, platforms):
    metrics.rect.y += metrics.yvel
    other = check_collisions(metrics, platforms)
    if not other is None:
        metrics.yvel = 0
        metrics.rect.bottom = other.rect.top
    elif metrics.yvel <= 30:
        metrics.yvel += 0.3
