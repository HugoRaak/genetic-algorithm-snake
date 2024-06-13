import time

import numpy as np
from tensorflow.keras import backend as K


def avg_steps_between_eating(steps_between_eating):
    return round(np.mean(np.array(steps_between_eating)), 2) if len(steps_between_eating) > 0 else 0


def fitness_func(best_score, nb_deaths, steps_between_eating, penalties):
    return round(((best_score * 5000)
            - (nb_deaths * 150)
            - (avg_steps_between_eating(steps_between_eating) * 100)
            - (penalties * 1000)), 2)


class Individual:
    def __init__(self, game, model, input_size, generation_id, individual_id):
        self.game = game
        self.model = model
        self.state_size = input_size
        self.generation_id = generation_id
        self.individual_id = individual_id

    # Get current state of the game in form of an input for the neural network
    def get_state(self):
        head_x, head_y = self.game.snake[0]
        apple_x, apple_y = self.game.apple
        state = [
            head_x + 1 < self.game.width + 2 and self.game.grid[head_y][head_x + 1] == 1,  # danger right
            head_x + -1 >= 0 and self.game.grid[head_y][head_x - 1] == 1,  # danger left
            head_y + -1 >= 0 and self.game.grid[head_y - 1][head_x] == 1,  # danger up
            head_y + 1 < self.game.height + 2 and self.game.grid[head_y + 1][head_x] == 1,  # danger down
            self.game.direction == self.game.right,
            self.game.direction == self.game.left,
            self.game.direction == self.game.up,
            self.game.direction == self.game.down,
            apple_x < head_x,  # food left
            apple_x > head_x,  # food right
            apple_y < head_y,  # food up
            apple_y > head_y  # food down
        ]
        for i in range(len(state)):
            if state[i]:
                state[i] = 1
            else:
                state[i] = 0
        return np.asarray(state).reshape(1, self.state_size)

    def train_game(self, steps_per_game=500, max_steps_to_get_food=50):
        steps = 0
        prev_score = 0
        steps_to_get_food = 0
        nb_deaths = 0
        best_score = 0
        steps_between_eating = []
        penalties = 0
        scores = []
        K.clear_session()
        self.game.reset()
        while steps < steps_per_game:
            need_reset = False
            state = self.get_state()
            prediction = self.model.predict(state, verbose=0)
            direction = np.argmax(prediction[0])
            score, is_dead = self.game.do_step(direction)

            if prev_score != score:
                prev_score = score
                steps_between_eating.append(1 if steps_to_get_food == 0 else steps_to_get_food)
                steps_to_get_food = 0
            elif is_dead:
                nb_deaths += 1
                need_reset = True
            elif steps_to_get_food >= max_steps_to_get_food:
                penalties += 1
                need_reset = True
            else:
                steps_to_get_food += 1

            if need_reset:
                scores.append(score)
                if score > best_score:
                    best_score = score
                prev_score = 0
                steps_to_get_food = 0
                self.game.reset()
            steps += 1

        fitness = fitness_func(best_score, nb_deaths, steps_between_eating, penalties)
        self.print_evaluation(fitness, best_score, nb_deaths, steps_between_eating, penalties)
        return fitness, round(np.mean(np.array(scores)), 2), nb_deaths, best_score

    def play_game(self):
        self.game.reset()
        self.game.draw()
        K.clear_session()
        self.game.root.after(200, self.step)

    def step(self):
        if not self.game.running:
            return
        state = self.get_state()
        prediction = self.model.predict(state, verbose=0)
        direction = np.argmax(prediction[0])
        _, is_dead = self.game.do_step(direction)
        if is_dead:
            self.game.reset()
            self.game.draw()
        self.game.root.after(200, self.step)

    def print_evaluation(self, fitness, best_score, nb_deaths, steps_between_eating, penalties):
        print("Generation: ", self.generation_id,
              " Individual: ", self.individual_id,
              " Fitness: ", fitness)
        print("Detailed evaluation: Best score: ", best_score,
              " Nb deaths: ", nb_deaths,
              " Avg steps between eating: ", avg_steps_between_eating(steps_between_eating),
              " Penalties: ", penalties)
