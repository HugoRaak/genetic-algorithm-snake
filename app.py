import numpy as np
import time
from model import Model
from game import Game
from individual import Individual


INDIVIDUAL_PER_POPULATION = 5
NB_GENERATIONS = 1


def run_population(population_weights, model_builder, simulation, generation_id):
    fitness_arr = []
    for i in range(INDIVIDUAL_PER_POPULATION):
        start_time = time.time()
        individual = Individual(
            game=simulation,
            model=model_builder.build_model(population_weights[i]),
            input_size=model_builder.layers[0],
            generation_id=generation_id,
            individual_id=i
        )
        fitness = individual.play_game()
        fitness_arr.append(fitness)
        individual.print_evaluation(fitness)
        print("Temps d'entraînement: ", round(time.time() - start_time, 2), "s")
    return np.array(fitness_arr)


if __name__ == "__main__":
    game = Game()
    model = Model()
    population_size = (INDIVIDUAL_PER_POPULATION, model.nb_weights)
    current_population_weights = np.random.choice(np.arange(-1, 1, step=0.01), size=population_size, replace=True)

    for generation in range(NB_GENERATIONS):
        fitness_arr = run_population(current_population_weights, model, game, generation)

        # update population weights