import pygame
import numpy as np
from libraryBantuan.nameValue import RGB, Point, CELL_DATA, Color
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
        self.text  = pygame.font.SysFont(name='woff', size=CELL_DATA[index].text_size).render(text, True, CELL_DATA[index].text_color)

class Game2048:
    def __init__(self, screen_width=480, screen_height=640, speed=40, n=4, m=4):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = speed
        self.n = n
        self.m = m
        self.high_score = 0
        
        self.padding = 10 
        board_size = (self.screen_width-4*self.padding, self.screen_height-200-2*self.padding)
        self.cell_size = ((board_size[0]-(m+1)*self.padding)/m, (board_size[1]-(n+1)*self.padding)/m)
    
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.board  = pygame.Rect((2*self.padding, 200), board_size)
        pygame.display.set_caption("Game 2048 by Rama Bena")
        self.screen.fill(Color.BACKGROUND)

        #* Tombol undo dan restart
        button_width  = 50
        button_height = 50
        restart_img = pygame.image.load('img/restart.png')
        restart_board_left = self.board.right - 6*self.padding - button_width
        restart_board_top  = self.board.top - 2*self.padding - button_height
        self.restart_board = pygame.draw.rect(self.screen, Color.BOARD,
                                               (restart_board_left, restart_board_top, button_width, button_height),
                                               border_radius=5)
        self.screen.blit(restart_img, restart_img.get_rect(center=self.restart_board.center))
        
        undo_img = pygame.image.load('img/undo.png')
        undo_board_left = self.restart_board.left - 4*self.padding - button_width
        undo_board_top  = self.board.top - 2*self.padding - button_height
        undo_board = pygame.draw.rect(self.screen, Color.BOARD,
                                         (undo_board_left, undo_board_top, button_width, button_height),
                                         border_radius=5)
        self.screen.blit(undo_img, undo_img.get_rect(center=undo_board.center))

        self.reset()

    #* ----------------------------- Public Method ---------------------------- #
    def reset(self):
        self.score = 0
        # buat matrix kosong
        self.matrix = []

        y = self.board.top + self.padding
        while y < self.board.bottom:
            row = []
            x = self.board.left + self.padding
            while x < self.board.right:
                row.append(Cell(x, y))
                x += self.cell_size[0]+self.padding
            self.matrix.append(row)
            y += self.cell_size[1]+self.padding

        # # isi cell random 2 kali
        self._place_random_cell()
        self._place_random_cell()

        # Update UI
        # self._testing()
        self._update_ui()

    def play(self):
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
                
                if next_cell == -1:                               # Taruh di akhir
                    can_move = True
                    matrix[0][j].set_value(value_now)
                    matrix[i][j].set_value(1)

                elif matrix[next_cell][j].value == value_now:    # Cell nya sama
                    can_move = True
                    matrix[i][j].set_value(1)
                    if not already_collision:       # Belum pernah collision
                        already_collision = True
                        matrix[next_cell][j].set_value(2*value_now)
                        self.score += (2*value_now)
                    else:               # kalau sudah pernah collicion -> taruh disampingnya
                        matrix[next_cell+1][j].set_value(value_now)

                elif (matrix[next_cell][j].value != value_now) and (next_cell != i-1):    # ada cell, cell nya beda dan tidak disamping
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
                
                elif matrix[i][next_cell].value == value_now:    # Cell nya sama
                    can_move = True
                    matrix[i][j].set_value(1)
                    if not already_collision:       # Belum pernah collision
                        already_collision = True
                        matrix[i][next_cell].set_value(2*value_now)
                        self.score += (2*value_now)
                    else:                           # kalau sudah pernah collicion -> taruh disampingnya
                        matrix[i][next_cell-1].set_value(value_now)
                
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
                
                if next_cell == len(matrix):                               # Taruh di akhir
                    can_move = True
                    matrix[len(matrix)-1][j].set_value(value_now)
                    matrix[i][j].set_value(1)
                elif matrix[next_cell][j].value == value_now:           # Cell nya sama
                    can_move = True
                    matrix[i][j].set_value(1)
                    if not already_collision:
                        already_collision = True
                        matrix[next_cell][j].set_value(2*value_now)
                        self.score += (2*value_now)
                    else:
                        matrix[next_cell-1][j].set_value(value_now)

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
                
                if next_cell == -1:                               # Taruh di akhir
                    can_move = True
                    matrix[i][0].set_value(value_now)
                    matrix[i][j].set_value(1)
               
                elif matrix[i][next_cell].value == value_now:    # Cell nya sama
                    can_move = True
                    matrix[i][j].set_value(1)
                    if not already_collision:
                        already_collision = True
                        matrix[i][next_cell].set_value(2*value_now)
                        self.score += (2*value_now)
                    else:
                        matrix[i][next_cell+1].set_value(value_now)

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
        #* Gambar Score dan High Score
        score_board_width  = 150 #? angka ngasal
        score_board_height = 50 #? angka ngasal
        scores = [
            {
                'board_left' : self.screen.get_rect().centerx - 2*self.padding - score_board_width,
                'board_top'  : self.screen.get_rect().top + 4*self.padding, 
                'text'       : "SCORE",
                'value'      : str(self.score)
            },
            {
                'board_left' : self.screen.get_rect().centerx + 2*self.padding,
                'board_top'  : self.screen.get_rect().top + 4*self.padding, 
                'text'       : "HIGH SCORE",
                'value'      : str(self.high_score)
            }
        ]

        for score in scores:
            # Gambar kotak di belakang skor
            score_board = pygame.draw.rect(self.screen, Color.BOARD, 
                                           (score['board_left'], score['board_top'], score_board_width, score_board_height), 
                                           border_radius=5)
            # Judul Skor
            score_text = pygame.font.SysFont(name='woff', size=20).render(score['text'], True, Color.BACKGROUND)
            self.screen.blit(score_text, score_text.get_rect(midtop=(score_board.centerx, score_board.top+self.padding)))
            # Nilai skor
            score_number = pygame.font.SysFont(name='woff', size=30).render(score['value'], True, Color.BACKGROUND)
            self.screen.blit(score_number, score_number.get_rect(midbottom=score_board.midbottom))
       

        #* Warnain kotak game
        pygame.draw.rect(self.screen, Color.BOARD, self.board, border_radius=20)

        #* Setiap block nya
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                cell  = self.matrix[i][j]
                # Gambar block
                block = pygame.draw.rect(self.screen, cell.color, 
                                         (cell.point.x, cell.point.y, self.cell_size[0], self.cell_size[1]), 
                                         border_radius=5)
                # Gambar nilai di block
                text = cell.text.get_rect(center=block.center)
                self.screen.blit(cell.text, text)
                
        #* update semuanya
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
        is_running = game.play()
        
    print("PERMAINAN SELESAI")
if __name__ == "__main__":
    main()