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
        self.direction = None


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

    def _move(self, direction):
        print("before")
        print(self.blocks)
        blocks_to_send = np.empty((0,2), dtype=int)
        for row in range(0,4):
            for col in range(0,4):
                if self.blocks[row,col]:
                    blocks_to_send = np.append(blocks_to_send,np.array([[row,col]]),axis=0)
        # print(blocks_to_send)

        # sort based on what we want to enact first
        if len(blocks_to_send) < 2:
            sort_to_send = blocks_to_send
        elif direction == Direction.RIGHT:
            sort_to_send = blocks_to_send[blocks_to_send[0, :].argsort()]
        elif direction == Direction.LEFT:
            sort_to_send = blocks_to_send[-blocks_to_send[0, :].argsort()]
        elif direction == Direction.UP:
            sort_to_send = blocks_to_send[blocks_to_send[:, 0].argsort()]
        elif direction == Direction.DOWN:
            sort_to_send = blocks_to_send[-blocks_to_send[:, 0].argsort()]
        for block in sort_to_send:
            # print(block)
            collision, new_row, new_col = self._send_away(block[0],block[1], direction)
            if new_row != block[0] or new_col != block[1]:
                self.blocks[new_row, new_col] = self.blocks[block[0],block[1]]
                self.blocks[block[0],block[1]] = 0
        print("after")
        print(self.blocks)
        

    def _send_away(self, row, col, direction):
        collided = False
        new_row = row
        new_col = col
        if direction == Direction.RIGHT:
            while not collided:
                new_col = new_col+1
                if new_col > 3:
                    new_col = 3
                    return collided, new_row, new_col
                else:
                    if self.blocks[new_row,new_col] != 0:
                        collided = True
        if direction == Direction.LEFT:
            while not collided:
                new_col = new_col-1
                if new_col < 0:
                    new_col = 0
                    return collided, new_row, new_col
                else:
                    if self.blocks[new_row,new_col] != 0:
                        collided = True
        if direction == Direction.DOWN:
            while not collided:
                new_row = new_row+1
                if new_row > 3:
                    new_row = 3
                    return collided, new_row, new_col
                else:
                    if self.blocks[new_row,new_col] != 0:
                        collided = True
        if direction == Direction.UP:
            while not collided:
                new_row = new_row-1
                if new_row < 0:
                    new_row = 0
                    return collided, new_row, new_col
                else:
                    if self.blocks[new_row,new_col] != 0:
                        collided = True

        return collided, new_row, new_col
    


    # def find_contact(self, row, col, direction):
    #     collision = False
    #     new_row=row
    #     new_col=col
    #     if direction == Direction.UP:
    #         for row_i in range(0,row):
    #             if self.blocks[row_i, col]:
    #                 collision = True
    #                 new_row = row_i
    #         if not collision:
    #             new_row = 0
    #     elif direction == Direction.DOWN:
    #         for row_i in range(3, row):
    #             if self.blocks[row_i, col]:
    #                 collision = True
    #                 new_row = row_i
    #         if not collision:
    #             new_row = 3
    #     elif direction == Direction.RIGHT:
    #         for col_i in range(3, col+1):
    #             if self.blocks[row, col_i]:
    #                 collision = True
    #                 new_col = col_i
    #         if not collision:
    #             new_col = 3
    #     elif direction == Direction.LEFT:
    #         for col_i in range(0, col):
    #             if self.blocks[row, col_i]:
    #                 collision = True
    #                 new_col = col_i
    #         if not collision:
    #             new_col = 0
    #     print("New row/col",new_row,new_col)
    #     return collision,  new_row, new_col
        

    def play_step(self):
        self._update_ui()
        # print(self.blocks)
        self.clock.tick(SPEED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                print("hi")
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                    self._move(self.direction)
                    self.addBlock()
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                    self._move(self.direction)
                    self.addBlock()
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                    self._move(self.direction)
                    self.addBlock()
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN 
                    self._move(self.direction)
                    self.addBlock

if __name__ == '__main__':
    game = BlockGame()
    game_over = False
    # main game loop
    while True:
        game.play_step()


        if game_over == True:
            break
            # if game over we break

   