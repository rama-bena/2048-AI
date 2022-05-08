import pygame
import numpy as np
from libraryBantuan.nameValue import Color, Point
from IPython.display import display
import random

class Cell:
    def __init__(self, x, y):
        self.value = 1
        self.point = Point(x, y)
        self.color = Color.BLOCK_1
        self.font = pygame.font.SysFont('woff', 80)
        self.text  = self.font.render("", True, Color.TEXT_1)

    def next_value(self):
        if self.value == 1:
            self.value = 2
            self.color = Color.BLOCK_2
            self.text  = self.font.render("2", True, Color.TEXT_2)
        elif self.value == 2:
            self.value = 4
            self.color = Color.BLOCK_4
            self.text  = self.font.render("4", True, Color.TEXT_4)
        elif self.value == 4:
            self.value = 8
            self.color = Color.BLOCK_8
            self.text  = self.font.render("8", True, Color.TEXT_8)
        elif self.value == 8:
            self.value = 16
            self.color = Color.BLOCK_16
            self.text  = self.font.render("16", True, Color.TEXT_16)
        elif self.value == 16:
            self.value = 32
            self.color = Color.BLOCK_32
            self.text  = self.font.render("32", True, Color.TEXT_32)
         

class Game2048:
    def __init__(self, screen_width=400, screen_height=400, speed=40, width=4, height=4):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = speed
        self.width = width
        self.height = height
        self.block_size_width = self.screen_width // self.width
        self.block_size_height = self.screen_height // self.height
        self.padding = 20

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(Color.SCREEN)
        pygame.display.flip()

        self.reset()

    def reset(self):
        # buat matrix kosong
        self.matrix = []
        for x in range(self.padding//2, self.screen_height, self.block_size_height):
            row = []
            for y in range(self.padding//2, self.screen_width, self.block_size_width):
                row.append(Cell(x, y))
            self.matrix.append(row)
        
        # isi cell random 2 kali
        self._place_random_cell()
        self._place_random_cell()

        # Update UI
        self._update_ui()

    
    def _update_ui(self):
        for i in range(self.height):
            for j in range(self.width):
                cell = self.matrix[i][j]
                block = pygame.Rect((cell.point.x, cell.point.y), (self.block_size_width-self.padding, self.block_size_height-self.padding))
                point_text = (cell.point.x + self.padding, cell.point.y + self.padding)
                
                # gambar
                pygame.draw.rect(self.screen, cell.color, block)
                self.screen.blit(cell.text, point_text)
        # update semuanya
        pygame.display.flip()

    def _place_random_cell(self):
        candidate_cell = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j].value == 1:
                    candidate_cell.append(self.matrix[i][j])

        random_cell = random.choice(candidate_cell)
        random_cell.next_value()
        if random.randint(1, 100) <= 10:
            random_cell.next_value()


def main():
    game = Game2048()

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                is_running = False

if __name__ == "__main__":
    main()