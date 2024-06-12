import numpy as np
from tensorflow.keras import backend as K


class Individual:
    def __init__(self, game, model, input_size, generation_id, individual_id):
        self.game = game
        self.model = model
        self.state_size = input_size
        self.generation_id = generation_id
        self.individual_id = individual_id
        self.best_score = 0
        self.nb_deaths = 0
        self.steps_between_eating = []
        self.penalties = 0

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

    def play_game(self, steps_per_game=500, max_steps_to_get_food=50):
        steps = 0
        prev_score = 0
        steps_to_get_food = 0
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
                self.steps_between_eating.append(1 if steps_to_get_food == 0 else steps_to_get_food)
                steps_to_get_food = 0
            elif is_dead:
                self.nb_deaths += 1
                need_reset = True
            elif steps_to_get_food >= max_steps_to_get_food:
                self.penalties += 1
                need_reset = True
            else:
                steps_to_get_food += 1

            if need_reset:
                if score > self.best_score:
                    self.best_score = score
                prev_score = 0
                steps_to_get_food = 0
                self.game.reset()
            steps += 1

        return self.fitness_func()

    def avg_steps_between_eating(self):
        return np.mean(np.array(self.steps_between_eating)) if len(self.steps_between_eating) > 0 else 0

    def fitness_func(self):
        return round(((self.best_score * 500)
                - (self.nb_deaths * 15)
                - (self.avg_steps_between_eating() * 10)
                - (self.penalties * 100)), 2)

    def print_evaluation(self, fitness):
        print("Generation: ", self.generation_id,
              " Individual: ", self.individual_id,
              " Evaluation: ", fitness)
        print("Detailed evaluation: Best score: ", self.best_score,
              " Nb deaths: ", self.nb_deaths,
              " Avg steps between eating: ", self.avg_steps_between_eating(),
              " Penalties: ", self.penalties)
