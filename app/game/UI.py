from typing import List
import pygame
from collections import namedtuple

from libraryBantuan.nameValue import Color, FileName
from .cell import Cell

Size  = namedtuple('Size', ('width', 'height'))

class UserInterface:
    def __init__(self, screen_width=480, screen_height=640, row=4, column=4):
        self.screen_width  = screen_width
        self.screen_height = screen_height
        self.row           = row
        self.column        = column

        #* Variabel ukuran dalam UI
        self.padding     = 10
        button_size      = Size(50, 50)
        game_board_size  = Size(self.screen_width-4*self.padding, self.screen_height-200-2*self.padding)
        self.cell_size   = Size((game_board_size.width-(column+1)*self.padding)/column, (game_board_size.height-(row+1)*self.padding)/row)
    
        #* Init pygame dan buat window
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game 2048 by Rama Bena")
        self.screen.fill(Color.BACKGROUND)
        
        #* Variabel font
        # buat font lambat, jadi biar sekali inisialisasi saja
        self.font_20 = pygame.font.SysFont(name='woff', size=20)
        self.font_30 = pygame.font.SysFont(name='woff', size=30)
        self.font_100 = pygame.font.SysFont(name='woff', size=100)

        #* Score dan High Score
        self._update_score_high_score(0, 0)

        #* Buat game_board
        self.game_board  = pygame.Rect((2*self.padding, 200), game_board_size)

        #* Tombol restart
        restart_img = pygame.image.load(FileName.RESTART_IMG)
        restart_board_left = self.game_board.right - 6*self.padding - button_size.width
        restart_board_top  = self.game_board.top - 2*self.padding - button_size.height
        self.restart_board = pygame.draw.rect(self.screen, Color.BOARD,
                                               (restart_board_left, restart_board_top, button_size.width, button_size.height),
                                               border_radius=5)
        self.screen.blit(restart_img, restart_img.get_rect(center=self.restart_board.center))
        
        #* Tombol undo
        undo_img = pygame.image.load(FileName.UNDO_IMG)
        undo_board_left = self.restart_board.left - 4*self.padding - button_size.width
        undo_board_top  = self.game_board.top - 2*self.padding - button_size.height
        self.undo_board = pygame.draw.rect(self.screen, Color.BOARD,
                                           (undo_board_left, undo_board_top, button_size.width, button_size.height),
                                           border_radius=5)
        self.screen.blit(undo_img, undo_img.get_rect(center=self.undo_board.center))


        #* Buat informasi Cell ukuran row x column
        self.cell:List[List[Cell]] = [] # sengaja dikasi tipe data, biar ngoding lebih cepet tinggal enter enter
        # Setiap element buat object cell baru
        y = self.game_board.top + self.padding
        while y < self.game_board.bottom: # Pakai while karena x,y bisa float
            row = []
            x = self.game_board.left + self.padding
            while x < self.game_board.right:
                row.append(Cell(x, y))
                x += self.cell_size[0]+self.padding
            self.cell.append(row)
            y += self.cell_size[1]+self.padding

        pygame.display.flip()

    def update(self, matrix, score, high_score):
        self._update_score_high_score(score, high_score)
        self._update_matrix(matrix)
        pygame.display.flip()

    def _update_score_high_score(self, score, high_score):
        score_board_size = Size(150, 50) #? angka ngasal
        scores = [
            {
                'board_left' : self.screen.get_rect().centerx - 2*self.padding - score_board_size.width,
                'board_top'  : self.screen.get_rect().top + 4*self.padding, 
                'text'       : "SCORE",
                'value'      : str(int(score))
            },
            {
                'board_left' : self.screen.get_rect().centerx + 2*self.padding,
                'board_top'  : self.screen.get_rect().top + 4*self.padding, 
                'text'       : "HIGH SCORE",
                'value'      : str(int(high_score))
            }
        ]

        for score in scores:
            #* Gambar kotak di belakang skor
            score_board = pygame.draw.rect(self.screen, Color.BOARD, 
                                            (score['board_left'], score['board_top'], score_board_size.width, score_board_size.height), 
                                            border_radius=5)
            #* Judul Skor
            score_text = self.font_20.render(score['text'], True, Color.BACKGROUND)
            self.screen.blit(score_text, score_text.get_rect(midtop=(score_board.centerx, score_board.top+self.padding)))
            #* Nilai skor
            score_number = self.font_30.render(score['value'], True, Color.BACKGROUND)
            self.screen.blit(score_number, score_number.get_rect(midbottom=score_board.midbottom))

    def _update_matrix(self, matrix):
        #* Warnain kotak game
        pygame.draw.rect(self.screen, Color.BOARD, self.game_board, border_radius=20)

        #* Setiap block nya
        for i in range(self.row):
            for j in range(self.column):
                self.cell[i][j].set_value(matrix[i][j]) # update nilai di cell
                cell = self.cell[i][j]                  # taruh di variabel biar lebih singkat
                
                #* Gambar cell block
                block = pygame.draw.rect(self.screen, cell.color, 
                                         (cell.point.x, cell.point.y, self.cell_size[0], self.cell_size[1]), 
                                         border_radius=5)
                #* Gambar nilai di block
                text = cell.text.get_rect(center=block.center)
                self.screen.blit(cell.text, text)

    def game_over(self):
        game_over_surface = pygame.Surface(self.game_board.size)
        game_over_surface.set_alpha(128)                         # tingkat transparan
        game_over_surface.fill(Color.BOARD)
    
        self.screen.blit(game_over_surface, self.game_board.topleft)

        game_over_text = self.font_100.render("GAME OVER", True, Color.BACKGROUND)
        self.screen.blit(game_over_text, game_over_text.get_rect(center=self.game_board.center))
        pygame.display.flip()