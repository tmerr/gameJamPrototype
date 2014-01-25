# code based off http://www.nandnor.net/?p=64

import pygame
import math
from pygame import *
from entities import *

DISPLAY = (800, 640)
DEPTH = 32
FLAGS = 0

# in blocks, 25 x 20

def main():
    pygame.init()
    screen = display.set_mode(DISPLAY, FLAGS, DEPTH)
    display.set_caption("Use arrows to move!")
    timer = time.Clock()
    
    up = down = left = right = False
    bg = Surface((32,32))
    bg.convert()
    bg.fill(Color("#000000"))
    entities = pygame.sprite.Group()
    
    swarm = Swarm()
    #player = Player(32, 32)
    platforms = []
    
    x = y = 0
    level = [
    "PPPPPPPPPPPPPPPPPPPPPPPPP",
    "P  P                    P",
    "P  PPPPPP               P",
    "P  P     P    P         P",
    "P  P      P   P         P",
    "P  P       P  P         P",
    "P  P         PP    PPPPPP",
    "P  P        P P         P",
    "P  P       P  P         P",
    "P  P      P   PPPPPP    P",
    "P  P     P    PP        P",
    "P  P PP       PPP      PP",
    "P  PPPPP      PPPP    PPP",
    "P       P     PPPPP  PPPP",
    "P        PP   P         P",
    "P            PP         P",
    "P          PP P         P",
    "P       PP    P         P",
    "P      PPPP   PE        P",
    "PPPPPPPPPPPPPPPPPPPPPPPPP",]
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            x += 32
        y += 32
        x = 0
    
    #entities.add(player)
    for guy in swarm.get_guys():
        entities.add(guy)
    
    while 1:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                raise(SystemExit)
            if e.type == KEYDOWN and e.key == K_ESCAPE: 
                raise(SystemExit)
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
        
        # draw background
        for y in range(20):
            for x in range(25):
                screen.blit(bg, (x * 32, y * 32))
        
        # update player, draw everything else
        swarm.update(platforms)
        #player.update(up, down, left, right, platforms)
        entities.draw(screen)
        
        pygame.display.flip()

        
if(__name__ == "__main__"):
    main()
