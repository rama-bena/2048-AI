import pygame
import numpy as np
from libraryBantuan.nameValue import CELL_DATA, Point
from IPython.display import display
import random

class Cell:
    def __init__(self, x, y):
        self.point = Point(x, y)
        self.set_value()

    def set_value(self, value=1):
        index = int(np.log2(value))
        self.value = CELL_DATA[index].value
        self.color = CELL_DATA[index].color
        text = "" if self.value == 1 else str(self.value)
        self.text  = pygame.font.SysFont('woff', CELL_DATA[index].text_size).render(text, True, CELL_DATA[index].text_color)

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
        pygame.display.set_caption("Game 2048 by Rama Bena")
        self.reset()

    #* ----------------------------- Public Method ---------------------------- #
    def reset(self):
        # buat matrix kosong
        self.matrix = []
        for y in range(self.padding//2, self.screen_width, self.block_size_width):
            row = []
            for x in range(self.padding//2, self.screen_height, self.block_size_height):
                row.append(Cell(x, y))
            self.matrix.append(row)
        
        # isi cell random 2 kali
        self._place_random_cell()
        self._place_random_cell()

        # Update UI
        self._update_ui()

    def keyboard_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Pencet exit
                return False
            if event.type == pygame.KEYDOWN: # Keyboard ditekan
                if event.key == pygame.K_UP:
                    print("atas")
                    can_move = self._move_up()
                    if can_move:
                        self._place_random_cell()
                        self._update_ui()
                if event.key == pygame.K_RIGHT:
                    print("kanan")
                    can_move = self._move_right()
                    if can_move:
                        self._place_random_cell()
                        self._update_ui()
                if event.key == pygame.K_DOWN:
                    print("bawah")
                    can_move = self._move_down()
                    if can_move:
                        self._place_random_cell()
                        self._update_ui()
                if event.key == pygame.K_LEFT:
                    print("kiri")
                    can_move = self._move_left()
                    if can_move:
                        self._place_random_cell()
                        self._update_ui()
        return True

    #* ---------------------------- Private Method ---------------------------- #
    def _move_up(self):
        matrix = self.matrix
        can_move = False
        for j in range(len(matrix[0])):
            already_collision = False
            for i in range(1, len(matrix)):
                value_now = matrix[i][j].value
                if value_now == 1:
                    continue
                next_cell = i-1
                while matrix[next_cell][j].value == 1:
                    next_cell -= 1
                    if next_cell == -1: # keluar batas
                        break
                
                if next_cell == -1:                               # keluar batas
                    can_move = True
                    matrix[0][j].set_value(value_now)
                    matrix[i][j].set_value(1)
                elif (matrix[next_cell][j].value==value_now) and (not already_collision):    # ada cell, cell nya sama
                    can_move = True
                    already_collision = True
                    matrix[next_cell][j].set_value(2*value_now)
                    matrix[i][j].set_value(1)
                elif (matrix[next_cell][j].value != value_now) and (next_cell != i-1):    # ada cell, cell nya beda
                    can_move = True
                    matrix[next_cell+1][j].set_value(value_now)
                    matrix[i][j].set_value(1)
        return can_move

    def _move_right(self):
        matrix = self.matrix
        can_move = False
        for i in range(len(matrix)):
            already_collision = False
            for j in range(len(matrix[i])-2, -1, -1):
                value_now = matrix[i][j].value
                if value_now == 1:
                    continue
                next_cell = j+1
                while matrix[i][next_cell].value == 1:
                    next_cell += 1
                    if next_cell == len(matrix[i]): # keluar batas
                        break
                
                if next_cell == len(matrix[i]):                               # keluar batas
                    can_move = True
                    matrix[i][len(matrix[i])-1].set_value(value_now)
                    matrix[i][j].set_value(1)
                elif (matrix[i][next_cell].value==value_now) and (not already_collision):    # ada cell, cell nya sama
                    can_move = True
                    already_collision = True
                    matrix[i][next_cell].set_value(2*value_now)
                    matrix[i][j].set_value(1)
                elif (matrix[i][next_cell].value != value_now) and (next_cell != j+1):                                             # cell nya beda dan tidak disamping
                    can_move = True
                    matrix[i][next_cell-1].set_value(value_now)
                    matrix[i][j].set_value(1)
        return can_move
    
    def _move_down(self):
        matrix = self.matrix
        can_move = False
        for j in range(len(matrix[0])):
            already_collision = False
            for i in range(len(matrix)-2, -1, -1):
                value_now = matrix[i][j].value
                if value_now == 1:
                    continue
                next_cell = i+1
                while matrix[next_cell][j].value == 1:
                    next_cell += 1
                    if next_cell == len(matrix): # keluar batas
                        break
                
                if next_cell == len(matrix):                               # keluar batas
                    can_move = True
                    matrix[len(matrix)-1][j].set_value(value_now)
                    matrix[i][j].set_value(1)
                elif (matrix[next_cell][j].value==value_now) and (not already_collision):    # ada cell, cell nya sama
                    can_move = True
                    already_collision = True
                    matrix[next_cell][j].set_value(2*value_now)
                    matrix[i][j].set_value(1)
                elif (matrix[next_cell][j].value != value_now) and (next_cell != i+1):    # ada cell, cell nya beda
                    can_move = True
                    matrix[next_cell-1][j].set_value(value_now)
                    matrix[i][j].set_value(1)
        return can_move
    
    def _move_left(self):
        matrix = self.matrix
        can_move = False
        for i in range(len(matrix)):
            already_collision = False
            for j in range(1, len(matrix[i])):
                value_now = matrix[i][j].value
                if value_now == 1:
                    continue
                next_cell = j-1
                while matrix[i][next_cell].value == 1:
                    next_cell -= 1
                    if next_cell == -1: # keluar batas
                        break
                
                if next_cell == -1:                               # keluar batas
                    can_move = True
                    matrix[i][0].set_value(value_now)
                    matrix[i][j].set_value(1)
                elif (matrix[i][next_cell].value==value_now) and (not already_collision):    # ada cell, cell nya sama
                    can_move = True
                    already_collision = True
                    matrix[i][next_cell].set_value(2*value_now)
                    matrix[i][j].set_value(1)
                elif (matrix[i][next_cell].value != value_now) and (next_cell != j-1):                                             # ada cell, cell nya beda
                    can_move = True
                    matrix[i][next_cell+1].set_value(value_now)
                    matrix[i][j].set_value(1)
        return can_move

    def _place_random_cell(self):
        candidate_cell = []
        # ambil semua cell kosong
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j].value == 1:
                    candidate_cell.append(self.matrix[i][j])
        
        # pilih salah satu dari semua cell kosong
        random_cell = random.choice(candidate_cell)
        if random.randint(1, 100) <= 10: # 10% kemungkinan muncul cell 4
            random_cell.set_value(4)
        else:
            random_cell.set_value(2)

    def _update_ui(self):
        # Warnain background
        self.screen.fill((187,173,160))

        # Setiap block nya
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                cell       = self.matrix[i][j]
                block      = pygame.Rect((cell.point.x, cell.point.y), (self.block_size_width-self.padding, self.block_size_height-self.padding))
                point_text = (cell.point.x + self.padding, cell.point.y + self.padding)
                
                # Gambar Block dan text nya
                pygame.draw.rect(self.screen, cell.color, block)
                self.screen.blit(cell.text, point_text)
        # update semuanya
        pygame.display.flip()

    def _testing(self):
        now = 4
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j].set_value(now)
                now *= 2



def main():
    game = Game2048()

    is_running = True
    while is_running:
        is_running = game.keyboard_listener()
        
    print("PERMAINAN SELESAI")
if __name__ == "__main__":
    main()