import numpy as np
from model import Model
from game import Game
from individual import Individual
from ag import *


INDIVIDUAL_PER_POPULATION = 5
NB_GENERATIONS = 2
NB_SELECTED_INDIVIDUALS = 2
NB_MUTATIONS = 1


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


if __name__ == "__main__":
    game = Game()
    model = Model()
    population_size = (INDIVIDUAL_PER_POPULATION, model.nb_weights)
    current_population_weights = np.random.choice(np.arange(-1, 1, step=0.01), size=population_size, replace=True)

    for generation in range(NB_GENERATIONS):
        population_fitness = run_population(current_population_weights, model, game, generation)
        selected_individuals = select_individuals(
            pop_weights=current_population_weights,
            pop_fitness=population_fitness,
            nb_selected=NB_SELECTED_INDIVIDUALS
        )
        children_from_crossover = crossover(
            parents=selected_individuals,
            children_size=(INDIVIDUAL_PER_POPULATION - NB_SELECTED_INDIVIDUALS, model.nb_weights)
        )
        children_from_mutation = mutation(children_from_crossover, NB_MUTATIONS)
        current_population_weights[0:NB_SELECTED_INDIVIDUALS, :] = selected_individuals
        current_population_weights[NB_SELECTED_INDIVIDUALS:, :] = children_from_mutation
