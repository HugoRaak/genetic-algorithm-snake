import math

import numpy as np
import time
from model import Model
from game import Game
from individual import Individual


if __name__ == "__main__":
    individual_per_population = 10
    nb_generations = 1
    model = Model()
    population_size = (individual_per_population, model.nb_weights)
    current_population_weights = np.random.choice(np.arange(-1, 1, step=0.01), size=population_size, replace=True)
    game = Game()

    for generation in range(nb_generations):
        for i in range(individual_per_population):
            start_time = time.time()
            individual = Individual(
                game=game,
                model=model.build_model(current_population_weights[i]),
                input_size=model.layers[0],
                generation_id=generation,
                individual_id=i
            )
            individual.play_game()
            individual.print_evaluation()
            print("Temps d'entraînement: ", round(time.time() - start_time, 2), "s")
        # update population weights