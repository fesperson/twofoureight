import pygame
import random

from collections import namedtuple
import numpy as np
import math
from enum import Enum

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

SQUARE_LENGTH = 100
SPEED = 40
BLACK = (0, 0, 0)
WHITE = (255,255,255)
YELLOW = (255,255,197)
ORANGE = (255,69,0)

# initialise modules
pygame.init()
font = pygame.font.Font('Roboto-Medium.ttf', 25)

class Block:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos


class BlockGame:
    def __init__(self, w=480, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('2048')
        self.clock = pygame.time.Clock()
        # Define the center coordinates
        x_coords = np.array([60, 180, 300, 420])
        y_coords = np.array([60, 180, 300, 420])
        # Create the grid of center points
        self.grid_centers = np.array([[Point(x, y) for x in x_coords] for y in y_coords])
        print(self.grid_centers)
        self.reset()


    def addBlock(self):
        pos_x = random.randint(0,3)
        pos_y = random.randint(0,3)
        if self.blocks[pos_x, pos_y]:
            self.addBlock()
        else:
            val = random.randint(1,2) * 2
            self.blocks[pos_x, pos_y] = val
    
    def reset(self):
        self.blocks = np.empty([4,4])
        self.addBlock()
        self.addBlock()
    
    def _update_ui(self):
        self.display.fill(WHITE)
        for r in range(0,4):
            for c in range(0,4):
                x = self.grid_centers[r,c][0]
                y = self.grid_centers[r,c][1] 
                if self.blocks[r,c]:
                    
                    pygame.draw.rect(self.display, 
                                    ORANGE, 
                                    pygame.Rect(x-SQUARE_LENGTH//2,
                                                y-SQUARE_LENGTH//2,
                                                SQUARE_LENGTH,
                                                SQUARE_LENGTH))
                    text = font.render(str(int(self.blocks[r,c])), True, BLACK)
                    text_rect = text.get_rect(center=(x, y))
                    self.display.blit(text, text_rect)
                else:
                    pygame.draw.rect(self.display, 
                                    YELLOW, 
                                    pygame.Rect(x-SQUARE_LENGTH/2,
                                                y-SQUARE_LENGTH/2,
                                                SQUARE_LENGTH,
                                                SQUARE_LENGTH))
        
        pygame.display.flip()
                
    def play_step(self):
        self._update_ui()
        print(self.blocks)
        self.clock.tick(SPEED)
        

if __name__ == '__main__':
    game = BlockGame()
    game_over = False
    # main game loop
    while True:
        game.play_step()


        if game_over == True:
            break
            # if game over we break

   