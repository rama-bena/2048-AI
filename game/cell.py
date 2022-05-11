import pygame
import numpy as np
from collections import namedtuple
from libraryBantuan.nameValue import CELL_DATA

Point = namedtuple('Point', ('x', 'y'))

class Cell:
    def __init__(self, x, y):
        self.point = Point(x, y)
        self.set_value()

    def set_value(self, value=1):
        index = int(np.log2(value))
        self.value = CELL_DATA[index].value
        self.color = CELL_DATA[index].color
        text = "" if self.value == 1 else str(self.value)
        self.text  = pygame.font.SysFont(name='woff', size=CELL_DATA[index].text_size).render(text, True, CELL_DATA[index].text_color)