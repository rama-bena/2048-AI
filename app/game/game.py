import numpy as np
import random
import copy 

from libraryBantuan.nameValue import Move, FileName
from .UI import UserInterface



class Game2048:
    def __init__(self, screen_width=480, screen_height=640, row=4, column=4):
        self.row = row
        self.column = column
        self.ui = UserInterface(screen_width=480, screen_height=640, row=4, column=4)
        self.high_score = 0
        self.n_games = 0
        self.reset()
    #* ----------------------------- Public Method ---------------------------- #
    def reset(self):
        self.n_games += 1
        self.iteration = 0
        self.score = 0
        self.matrix = [[0 for j in range(self.column)] for i in range(self.row)]
        
        #* isi cell random 2 kali
        self._place_random_cell()
        self._place_random_cell()

        #* Update UI
        self.ui.update(self.matrix, self.score, self.high_score)
    
    def play(self, action):
        self.iteration += 1
        reward = 0

        #* Lakukan action
        next_matrix = copy.deepcopy(self.matrix)
        plus_score  = 0
        if action == Move.UP:
            next_matrix, plus_score = self._move_up(next_matrix)
        elif action == Move.RIGHT:
            next_matrix, plus_score = self._move_right(next_matrix)
        elif action == Move.DOWN:
            next_matrix, plus_score = self._move_down(next_matrix)
        elif action == Move.LEFT:
            next_matrix, plus_score = self._move_left(next_matrix)
        
        if next_matrix != self.matrix:
            self.iteration = 0
            self.matrix = next_matrix
            self._place_random_cell()

            self.score += plus_score
            if self.score > self.high_score:
                self.high_score = self.score

        state = self.get_state()

        #* Cek game over
        game_over = self._is_game_over()

        if game_over:
            reward = -1000
        else:
            reward = np.log2(plus_score) if plus_score!=0 else -100

        # update data ke file dan UI
        self.ui.update(self.matrix, self.score, self.high_score)
        
        return state, reward, game_over
        
    def get_state(self):
        state = []
        for i in range(self.row):
            for j in range(self.column):
                state.append(self.matrix[i][j])
        return state

    #* ---------------------------- Private Method ---------------------------- #
    def _move_up(self, matrix):
        plus_score = 0
        for j in range(self.column):
            already_collision = False
            for i in range(1, self.row):
                value_now = matrix[i][j]
                if value_now == 0:
                    continue
                next_cell = i-1
                while matrix[next_cell][j] == 0:
                    next_cell -= 1
                    if next_cell == -1: # keluar batas
                        break
                
                if next_cell == -1:                               # Taruh di akhir
                    matrix[0][j] = value_now
                    matrix[i][j] = 0
                elif matrix[next_cell][j] == value_now:    # Cell nya sama
                    matrix[i][j] = 0
                    if not already_collision:       # Belum pernah collision
                        already_collision = True
                        matrix[next_cell][j] = 2*value_now
                        plus_score += 2*value_now
                    else:               # kalau sudah pernah collicion -> taruh disampingnya
                        matrix[next_cell+1][j] = value_now
                elif (matrix[next_cell][j] != value_now) and (next_cell != i-1):    # ada cell, cell nya beda dan tidak disamping
                    matrix[next_cell+1][j] = value_now
                    matrix[i][j] = 0
        return (matrix, plus_score)

    def _move_right(self, matrix):
        plus_score = 0
        for i in range(self.row):
            already_collision = False
            for j in range(self.column-2, -1, -1):
                value_now = matrix[i][j]
                if value_now == 0:
                    continue
                next_cell = j+1
                while matrix[i][next_cell] == 0:
                    next_cell += 1
                    if next_cell == self.column: # keluar batas
                        break
                
                if next_cell == self.column:                               # keluar batas
                    matrix[i][self.column-1] = value_now
                    matrix[i][j] = 0
                elif matrix[i][next_cell] == value_now:    # Cell nya sama
                    matrix[i][j] = 0
                    if not already_collision:       # Belum pernah collision
                        already_collision = True
                        matrix[i][next_cell] = 2*value_now
                        plus_score += 2*value_now
                    else:                           # kalau sudah pernah collicion -> taruh disampingnya
                        matrix[i][next_cell-1] = value_now         
                elif (matrix[i][next_cell] != value_now) and (next_cell != j+1): # cell nya beda dan tidak disamping
                    matrix[i][next_cell-1] = value_now
                    matrix[i][j] = 0

        return (matrix, plus_score)
    
    def _move_down(self, matrix):
        plus_score = 0
        for j in range(self.column):
            already_collision = False
            for i in range(self.row-2, -1, -1):
                value_now = matrix[i][j]
                if value_now == 0:
                    continue
                next_cell = i+1
                while matrix[next_cell][j] == 0:
                    next_cell += 1
                    if next_cell == self.row: # keluar batas
                        break
                if next_cell == self.row:                               # Taruh di akhir
                    matrix[self.row-1][j] = value_now
                    matrix[i][j] = 0
                elif matrix[next_cell][j] == value_now:           # Cell nya sama
                    matrix[i][j] = 0
                    if not already_collision:
                        already_collision = True
                        matrix[next_cell][j] = 2*value_now
                        plus_score += 2*value_now
                    else:
                        matrix[next_cell-1][j] = value_now
                elif (matrix[next_cell][j] != value_now) and (next_cell != i+1):    # ada cell, cell nya beda
                    matrix[next_cell-1][j] = value_now
                    matrix[i][j] = 0

        return (matrix, plus_score)
    
    def _move_left(self, matrix):
        plus_score = 0
        for i in range(self.row):
            already_collision = False
            for j in range(1, self.column):
                value_now = matrix[i][j]
                if value_now == 0:
                    continue
                next_cell = j-1
                while matrix[i][next_cell] == 0:
                    next_cell -= 1
                    if next_cell == -1: # keluar batas
                        break
                
                if next_cell == -1:                               # Taruh di akhir
                    matrix[i][0] = value_now
                    matrix[i][j] = 0  
                elif matrix[i][next_cell] == value_now:    # Cell nya sama
                    matrix[i][j] = 0
                    if not already_collision:
                        already_collision = True
                        matrix[i][next_cell] = 2*value_now
                        plus_score += 2*value_now
                    else:
                        matrix[i][next_cell+1] = value_now
                elif (matrix[i][next_cell] != value_now) and (next_cell != j-1):                                             # ada cell, cell nya beda
                    matrix[i][next_cell+1] = value_now
                    matrix[i][j] = 0
        return (matrix, plus_score)

    def _place_random_cell(self):
        #* ambil semua cell kosong
        candidate_cell = []
        for i in range(self.row):
            for j in range(self.column):
                if self.matrix[i][j] == 0:
                    candidate_cell.append((i, j))
    
        #* pilih salah satu dari semua cell kosong
        random_cell = random.choice(candidate_cell)
        if random.randint(1, 100) <= 10: # 10% kemungkinan muncul cell 4
            self.matrix[random_cell[0]][random_cell[1]] = 4
        else:
            self.matrix[random_cell[0]][random_cell[1]] = 2

    def _is_game_over(self):
        # 1. jika ada cell kosong maka belum game over
        # 2. disetiap cell jika ada tetangga yang nilainya sama maka belum game over

        adjacent = [(-1, 0), (0, 1), (1, 0), (-1, 0)]
        for i in range(self.row):
            for j in range(self.column):
                if self.matrix[i][j] == 0:
                    return False
                for idx in range(4): # setiap tetangga nya
                    next_i = i+adjacent[idx][0]
                    next_j = j+adjacent[idx][1]
                    if (0 <= next_i < self.row) and (0 <= next_j < self.column): # masih dalam kotak
                        if self.matrix[i][j] == self.matrix[next_i][next_j]:
                            return False
        print('game over')
        return self.iteration >=10

    

    #* ---------------------------- testing method ---------------------------- #
    def print_matrix(self):
        for i in range(self.row):
            for j in range(self.column):
                print(self.matrix[i][j], end=' ')
            print()