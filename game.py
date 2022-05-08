import pygame
import numpy as np
from libraryBantuan.nameValue import Color

class game2048:
    def __init__(self, screen_width=640, screen_height=480, speed=40, width=4, height=4):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = speed
        self.width = width
        self.height = height
        self.block_size_width = self.screen_width // self.width
        self.block_size_height = self.screen_height // self.height

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(Color.SCREEN)
        pygame.display.flip()

        self.reset()

    def reset(self):
        self.matrix = np.zeros((self.height, self.width))
        
        
        
        padding = 20
        for i in range(padding, self.screen_width, self.block_size_width):
            for j in range(padding, self.screen_height, self.block_size_height):
                pygame.draw.rect(self.screen, Color.BLOCK_0, pygame.Rect((i, j), (self.block_size_width-padding, self.block_size_height-padding)))

        pygame.display.flip()


def main():
    game = game2048(screen_width=400, screen_height=400)

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                is_running = False

if __name__ == "__main__":
    main()