import pygame
from libraryBantuan.nameValue import Move
from game.game import Game2048


if __name__ == "__main__":
    game = Game2048()
    undo_button    = game.ui.undo_board
    restart_button = game.ui.restart_board

    click_pos = (0, 0)
    release_pos = (0, 0)

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
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                print('klik')
    
            if event.type == pygame.MOUSEBUTTONUP: # Klik
                release_pos = pygame.mouse.get_pos()
                print('lepas')
            else:
                release_pos = (0,0)
    
            if undo_button.collidepoint(click_pos) and undo_button.collidepoint(release_pos): # klik undo
                click_pos, release_pos = (0,0), (0,0)
                print('klik undo')
                game.undo()

            if restart_button.collidepoint(click_pos) and restart_button.collidepoint(release_pos): # klik restart
                click_pos = (0,0)
                print('klik restart')
                game.reset()
    print("PERMAINAN SELESAI")