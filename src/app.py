import os
import numpy as np
from model import Model
from game import Game
from individual import Individual
from ag import *


INDIVIDUAL_PER_POPULATION = 5
NB_GENERATIONS = 2
NB_SELECTED_INDIVIDUALS = 3
NB_MUTATIONS = 1
SAVE_WEIGHTS_INTERVAL = 5
CURRENT_GENERATION = 0
RESTORE_WEIGHTS_FROM_TXT = False
PATH_WEIGHTS = "weights/"
PATH_STATS = "stats/"


def run_population(population_weights, model_builder, simulation, generation_id):
    fitness_arr = []
    deaths_arr = []
    avg_score_arr = []
    best_score_arr = []
    for i in range(INDIVIDUAL_PER_POPULATION):
        individual = Individual(
            game=simulation,
            model=model_builder.build_model(population_weights[i]),
            input_size=model_builder.layers[0],
            generation_id=generation_id,
            individual_id=i
        )
        fitness, avg_score, deaths, best_score = individual.play_game()
        fitness_arr.append(fitness)
        avg_score_arr.append(avg_score)
        deaths_arr.append(deaths)
        best_score_arr.append(best_score)
    return (np.array(fitness_arr), np.array(avg_score_arr),
            round(np.mean(np.array(deaths_arr)), 2), np.array(best_score_arr))


if __name__ == "__main__":
    game = Game()
    model = Model()
    population_size = (INDIVIDUAL_PER_POPULATION, model.nb_weights)

    if RESTORE_WEIGHTS_FROM_TXT:
        path = PATH_WEIGHTS + "/generation_" + str(CURRENT_GENERATION) + ".txt"
        current_population_weights = np.loadtxt(path)
    else:
        current_population_weights = np.random.choice(np.arange(-1, 1, step=0.01), size=population_size, replace=True)

    for generation in range(NB_GENERATIONS):
        # run population
        population_fitness, avgs_score, avg_deaths, best_scores = run_population(current_population_weights, model, game, generation)

        # select individuals from population
        selected_individuals = select_individuals(
            pop_weights=current_population_weights,
            pop_fitness=population_fitness,
            nb_selected=NB_SELECTED_INDIVIDUALS
        )

        # create next generation
        children_from_crossover = crossover(
            parents=selected_individuals,
            children_size=(INDIVIDUAL_PER_POPULATION - NB_SELECTED_INDIVIDUALS, model.nb_weights)
        )
        children_from_mutation = mutation(children_from_crossover, NB_MUTATIONS)
        current_population_weights[0:NB_SELECTED_INDIVIDUALS, :] = selected_individuals
        current_population_weights[NB_SELECTED_INDIVIDUALS:, :] = children_from_mutation

        # save generation stats
        if not os.path.exists(PATH_STATS):
            os.makedirs(PATH_STATS)
        path = PATH_STATS + "/generations_stats.txt"
        f = open(path, "a+")
        f.write("Generation: " + str(generation) + "\n")
        f.write("Max fitness: " + str(np.max(population_fitness))
                + " Max avg score: " + str(np.max(avgs_score))
                + " Avg fitness: " + str(round(np.mean(population_fitness), 2))
                + " Avg deaths: " + str(avg_deaths)
                + " Avg avg score: " + str(round(np.mean(avgs_score), 2))
                + " Max score: " + str(np.max(best_scores))
                + " Best individual: " + str(np.argmax(population_fitness)) + " \n")
        f.close()

        # save weights
        if generation % SAVE_WEIGHTS_INTERVAL == 0 or generation == NB_GENERATIONS - 1:
            if not os.path.exists(PATH_WEIGHTS):
                os.makedirs(PATH_WEIGHTS)
            path = PATH_WEIGHTS + "/generation_" + str(generation) + ".txt"
            np.savetxt(path, current_population_weights)
