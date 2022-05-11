import pickle
import numpy as np
import random

from libraryBantuan.nameValue import Move, FileName
from .UI import UserInterface



class Game2048:
    def __init__(self, screen_width=480, screen_height=640, row=4, column=4):
        self.row = row
        self.column = column
        self.ui = UserInterface(screen_width=480, screen_height=640, row=4, column=4)

        #* Ambil high score dari file atau 0
        try:
            with open(FileName.HIGH_SCORE, 'r') as f:
                self.high_score = int(float(f.readline()))
        except:
            self.high_score = 0  

        #* Ambil matrix dan score dari file kalau ada, kalau tidak buat ulang
        try:
            with open(FileName.MATRIX, 'rb') as f:
                self.matrix = pickle.load(f)
                self.score = 0
                for row in self.matrix:
                    self.score += np.sum([i for i in row if i != 1])
            self.ui.update(self.matrix, self.score, self.high_score)
            self._print_matrix()
        except:
            self.reset()

    #* ----------------------------- Public Method ---------------------------- #
    def reset(self):
        self.score = 0
        
        self.matrix = [[1 for j in range(self.column)] for i in range(self.row)]

        # isi cell random 2 kali
        self._place_random_cell()
        self._place_random_cell()
        
        # simpan di file
        self._update_matrix()

        self.ui.update(self.matrix, self.score, self.high_score)
        self._print_matrix()

    def play(self, action):
        is_game_over = self._is_game_over()
        
        can_move = False
        if action == Move.UP:
            can_move = self._move_up()
        elif action == Move.RIGHT:
            can_move = self._move_right()
        elif action == Move.DOWN:
            can_move = self._move_down()
        elif action == Move.LEFT:
            can_move = self._move_left()
        
        if can_move:
            self._place_random_cell()
            if self.score > self.high_score:
                self._update_high_score()
            
            self._update_matrix()
            self.ui.update(self.matrix, self.score, self.high_score)
            self._print_matrix()
         

    #* ---------------------------- Private Method ---------------------------- #
    def _move_up(self):
        can_move = False
        for j in range(self.column):
            already_collision = False
            for i in range(1, self.row):
                value_now = self.matrix[i][j]
                if value_now == 1:
                    continue
                next_cell = i-1
                while self.matrix[next_cell][j] == 1:
                    next_cell -= 1
                    if next_cell == -1: # keluar batas
                        break
                
                if next_cell == -1:                               # Taruh di akhir
                    can_move = True
                    self.matrix[0][j] = value_now
                    self.matrix[i][j] = 1

                elif self.matrix[next_cell][j] == value_now:    # Cell nya sama
                    can_move = True
                    self.matrix[i][j] = 1
                    if not already_collision:       # Belum pernah collision
                        already_collision = True
                        self.matrix[next_cell][j] = 2*value_now
                        self.score += (2*value_now)
                    else:               # kalau sudah pernah collicion -> taruh disampingnya
                        self.matrix[next_cell+1][j] = value_now

                elif (self.matrix[next_cell][j] != value_now) and (next_cell != i-1):    # ada cell, cell nya beda dan tidak disamping
                    can_move = True
                    self.matrix[next_cell+1][j] = value_now
                    self.matrix[i][j] = 1
        return can_move

    def _move_right(self):
        can_move = False
        for i in range(self.row):
            already_collision = False
            for j in range(self.column-2, -1, -1):
                value_now = self.matrix[i][j]
                if value_now == 1:
                    continue
                next_cell = j+1
                while self.matrix[i][next_cell] == 1:
                    next_cell += 1
                    if next_cell == self.column: # keluar batas
                        break
                
                if next_cell == self.column:                               # keluar batas
                    can_move = True
                    self.matrix[i][self.column-1] = value_now
                    self.matrix[i][j] = 1
                
                elif self.matrix[i][next_cell] == value_now:    # Cell nya sama
                    can_move = True
                    self.matrix[i][j] = 1
                    if not already_collision:       # Belum pernah collision
                        already_collision = True
                        self.matrix[i][next_cell] = 2*value_now
                        self.score += (2*value_now)
                    else:                           # kalau sudah pernah collicion -> taruh disampingnya
                        self.matrix[i][next_cell-1] = value_now
                
                elif (self.matrix[i][next_cell] != value_now) and (next_cell != j+1):                                             # cell nya beda dan tidak disamping
                    can_move = True
                    self.matrix[i][next_cell-1] = value_now
                    self.matrix[i][j] = 1

        return can_move
    
    def _move_down(self):
        can_move = False
        for j in range(self.column):
            already_collision = False
            for i in range(self.row-2, -1, -1):
                value_now = self.matrix[i][j]
                if value_now == 1:
                    continue
                next_cell = i+1
                while self.matrix[next_cell][j] == 1:
                    next_cell += 1
                    if next_cell == self.row: # keluar batas
                        break
                
                if next_cell == self.row:                               # Taruh di akhir
                    can_move = True
                    self.matrix[self.row-1][j] = value_now
                    self.matrix[i][j] = 1
                elif self.matrix[next_cell][j] == value_now:           # Cell nya sama
                    can_move = True
                    self.matrix[i][j] = 1
                    if not already_collision:
                        already_collision = True
                        self.matrix[next_cell][j] = 2*value_now
                        self.score += (2*value_now)
                    else:
                        self.matrix[next_cell-1][j] = value_now

                elif (self.matrix[next_cell][j] != value_now) and (next_cell != i+1):    # ada cell, cell nya beda
                    can_move = True
                    self.matrix[next_cell-1][j] = value_now
                    self.matrix[i][j] = 1

        return can_move
    
    def _move_left(self):
        can_move = False
        for i in range(self.row):
            already_collision = False
            for j in range(1, self.column):
                value_now = self.matrix[i][j]
                if value_now == 1:
                    continue
                next_cell = j-1
                while self.matrix[i][next_cell] == 1:
                    next_cell -= 1
                    if next_cell == -1: # keluar batas
                        break
                
                if next_cell == -1:                               # Taruh di akhir
                    can_move = True
                    self.matrix[i][0] = value_now
                    self.matrix[i][j] = 1
               
                elif self.matrix[i][next_cell] == value_now:    # Cell nya sama
                    can_move = True
                    self.matrix[i][j] = 1
                    if not already_collision:
                        already_collision = True
                        self.matrix[i][next_cell] = 2*value_now
                        self.score += (2*value_now)
                    else:
                        self.matrix[i][next_cell+1] = value_now

                elif (self.matrix[i][next_cell] != value_now) and (next_cell != j-1):                                             # ada cell, cell nya beda
                    can_move = True
                    self.matrix[i][next_cell+1] = value_now
                    self.matrix[i][j] = 1
        return can_move

    def _place_random_cell(self):
        candidate_cell = []
        # ambil semua cell kosong
        for i in range(self.row):
            for j in range(self.column):
                if self.matrix[i][j] == 1:
                    candidate_cell.append((i, j))
    
        # pilih salah satu dari semua cell kosong
        random_cell = random.choice(candidate_cell)
        if random.randint(1, 100) <= 10: # 10% kemungkinan muncul cell 4
            self.matrix[random_cell[0]][random_cell[1]] = 4
        else:
            self.matrix[random_cell[0]][random_cell[1]] = 2

    def _is_game_over(self):
        adjacent = [(-1, 0), (0, 1), (1, 0), (-1, 0)]
        for i in range(self.row):
            for j in range(self.column):
                if self.matrix[i][j] == 1: # Cek jika masih kosong, belum game over
                    return False
                for idx in range(4): # Cek jika disekitarnya nilainya sama, belum game over
                    next_i = i+adjacent[idx][0]
                    next_j = j+adjacent[idx][1]
                    if (0 <= next_i < self.row) and (0 <= next_j < self.column): # masih dalam kotak
                        if self.matrix[i][j] == self.matrix[next_i][next_j]:
                            return False
        print('game over')
        return True

    def _update_high_score(self):
        self.high_score = self.score
        with open(FileName.HIGH_SCORE, 'w') as f:
            f.write(str(self.high_score))

    def _update_matrix(self):
        with open(FileName.MATRIX, 'wb') as f:
            pickle.dump(self.matrix, f)

    def _print_matrix(self):
        for i in range(self.row):
            for j in range(self.column):
                print(self.matrix[i][j], end=' ')
            print()

    def _testing(self):
        now = 4
        for i in range(self.row):
            for j in range(self.column):
                self.matrix[i][j] = now
                now *= 2