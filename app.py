import numpy as np
from model import Model
from game import Game
from individual import Individual


INDIVIDUAL_PER_POPULATION = 5
NB_GENERATIONS = 1
NB_SELECTED_INDIVIDUALS = 2


def run_population(population_weights, model_builder, simulation, generation_id):
    fitness_arr = []
    for i in range(INDIVIDUAL_PER_POPULATION):
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
    return np.array(fitness_arr)


def select_individuals(pop_weights, pop_fitness):
    tmp_fitness = np.array(pop_fitness, copy=True)
    selected = np.empty((NB_SELECTED_INDIVIDUALS, pop_weights.shape[1]))
    for selected_num in range(NB_SELECTED_INDIVIDUALS):
        max_fitness_idx = np.argmax(tmp_fitness)
        selected[selected_num, :] = pop_weights[max_fitness_idx, :]
        tmp_fitness[max_fitness_idx] = -np.inf
    return selected


if __name__ == "__main__":
    game = Game()
    model = Model()
    population_size = (INDIVIDUAL_PER_POPULATION, model.nb_weights)
    current_population_weights = np.random.choice(np.arange(-1, 1, step=0.01), size=population_size, replace=True)

    for generation in range(NB_GENERATIONS):
        population_fitness = run_population(current_population_weights, model, game, generation)
        selected_individuals = select_individuals(current_population_weights, population_fitness)
        # update population weights