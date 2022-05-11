import pygame
from libraryBantuan.nameValue import Move
from game.game import Game2048
from game.UI import UserInterface


if __name__ == "__main__":
    game = Game2048()
    ui = game.ui
    
    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Pencet exit
                is_running = False
           
            if event.type == pygame.KEYDOWN: # Keyboard ditekan
                if event.key == pygame.K_UP:
                    print("atas")
                    game.play(Move.UP)

                if event.key == pygame.K_RIGHT:
                    print("kanan")
                    game.play(Move.RIGHT)

                if event.key == pygame.K_DOWN:
                    print("bawah")
                    game.play(Move.DOWN)
                    
                if event.key == pygame.K_LEFT:
                    print("kiri")
                    game.play(Move.LEFT)
            
            if event.type == pygame.MOUSEBUTTONUP: # Klik
                pos = pygame.mouse.get_pos()
                print('klik')
                if ui.restart_board.collidepoint(pos): # klik restart
                    print('klik restart')
                    game.reset()


    print("PERMAINAN SELESAI")