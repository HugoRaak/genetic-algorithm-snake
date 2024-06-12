import numpy as np
import random

# select individuals to crossover for next generation
def select_individuals(pop_weights, pop_fitness, nb_selected):
    tmp_fitness = np.array(pop_fitness, copy=True)
    selected = np.empty((nb_selected, pop_weights.shape[1]))
    for selected_num in range(nb_selected):
        max_fitness_idx = np.argmax(tmp_fitness)
        selected[selected_num, :] = pop_weights[max_fitness_idx, :]
        tmp_fitness[max_fitness_idx] = -np.inf
    return selected


# creating children for next generation
def crossover(parents, children_size):
    children_weights = np.empty(children_size)
    for child_idx in range(children_size[0]):
        parent1_idx, parent2_idx = random.sample(range(parents.shape[0]), 2)
        crossover_mask = np.random.rand(children_size[1]) < 0.5
        children_weights[child_idx] = np.where(crossover_mask, parents[parent1_idx], parents[parent2_idx])
    return children_weights


# mutating the children generated from crossover to maintain variation in the population
def mutation(children_crossover, nb_mutations):
    for child_idx in range(children_crossover.shape[0]):
        for _ in range(nb_mutations):
            idx = random.randint(0, children_crossover.shape[1] - 1)
            random_value = np.random.choice(np.arange(-1, 1, step=0.001), size=1, replace=False)
            children_crossover[child_idx][idx] = children_crossover[child_idx][idx] + random_value
    return children_crossover
