import pygame
from libraryBantuan.nameValue import Move
from app.game.game import Game2048
from app.agent.agent import Agent
import time

if __name__ == "__main__":
    agent = Agent()
    game = Game2048()

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Pencet exit
                is_running = False
        
        state = game.get_state()
        print('STATE OLD')
        game.print_matrix()

        action = agent.find_action(state)
        print(f"Action : {action}")

        reward, game_over = game.play(action)
        print(f"Reward:{reward}; game_over:{game_over}")
        
        print("STATE NEW")
        next_state = game.get_state()
        game.print_matrix()
        print()

        agent.remember(state, action, reward, next_state, game_over)
        agent.train_short_memory(state, action, reward, next_state, game_over)

        if game_over:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
        
