import random
from collections import deque
from app.game.game import Game2048
# from app.model.model import *


class Agent:
    def __init__(self, max_memory=10_000):
        self.epsilon = 100
        self.n_games = 0
        self.memory = deque(maxlen=max_memory)

    #* ----------------------------- Public Method ---------------------------- #

    def find_action(self, state):
        final_move = [0, 0, 0, 0]
        # new_epsilon = self.epsilon - (2 * self.n_games)
        new_epsilon = 100
        if random.randint(1, 100) <= new_epsilon:
            idx = random.randint(0, 3)
            final_move[idx] = 1
        else:
            final_move = [1, 0, 0, 0]

        return final_move

    
    def remember(self, state_old, action, state, reward, game_over):
        if (state_old, action, state, reward, game_over) not in self.memory:
            self.memory.append((state_old, action, state, reward, game_over))

    def train_short_memory(self, state_old, action, state, reward, game_over):
        pass

    def train_long_memory(self):
        pass

    
    #* ---------------------------- Private Method ---------------------------- #