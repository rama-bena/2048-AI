import torch
import random
from collections import deque

from app.game.game import Game2048
from app.model.model import Linear_QNet, QTrainer


class Agent:
    def __init__(self, max_memory=1_000_000, batch_size=1000, epsilon=100, learning_rate=0.001, gamma=0.95):
        self.BATCH_SIZE = batch_size
        self.epsilon = 100
        self.n_games = 0
        self.memory = deque(maxlen=max_memory)
        self.model = Linear_QNet(16, 8, 8, 4)
        self.trainer = QTrainer(self.model, learning_rate, gamma=gamma)

    #* ----------------------------- Public Method ---------------------------- #

    def find_action(self, state):
        final_move = [0, 0, 0, 0]
        new_epsilon = self.epsilon - (1 * self.n_games)
        if random.randint(1, 100) <= new_epsilon:
            idx = random.randint(0, 3)
            final_move[idx] = 1
        else:
            # Jadikan bentuk tensor dulu statenya
            state = torch.tensor(state, dtype=torch.float)
            # Lakukan prediksi gerakan
            prediction = self.model(state)
            # Ambil gerakan yang nilainya paling tinggi
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    
    def remember(self, state, action, reward, next_state, game_over):
        if (state, action, reward, next_state, game_over) not in self.memory:
            self.memory.append((state, action, reward, next_state, game_over))

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def train_long_memory(self):
        mini_sample = self.memory #? gak pakek batch. Kode diatas pakai batch
        

        # Ekstrak setiap paramater lalu train
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    
    #* ---------------------------- Private Method ---------------------------- #