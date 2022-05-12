import pygame
from app.game.game import Game2048
from app.agent.agent import Agent
from libraryBantuan.plot import plot
import time

if __name__ == "__main__":
    # pygame.init()
    # pygame.font.init()

    agent = Agent()
    game = Game2048()
    total_reward = 0
    rewards = [0]
    total_score = 0
    scores = [0]

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Pencet exit
                is_running = False
        
        state = game.get_state()
        action = agent.find_action(state)
        score, reward, game_over = game.play(action)
        next_state = game.get_state()

        agent.remember(state, action, reward, next_state, game_over)
        agent.train_short_memory(state, action, reward, next_state, game_over)
        
        if game_over:
            rewards.append(total_reward)
            scores.append(total_score)
            plot(scores, rewards)
            agent.n_games += 1
            print(f"Games   : {agent.n_games}")
            print(f"Score   : {game.score}")
            new_epsilon = max(agent.epsilon - (1*agent.n_games), 0)
            print(f"random rate : {new_epsilon}%")
            print(f"Total reward : {total_reward}")
            print()
            
            total_reward = 0
            total_score = 0
            game.reset()
            agent.train_long_memory()
        else:
            total_reward += reward
            total_score  += score


        
