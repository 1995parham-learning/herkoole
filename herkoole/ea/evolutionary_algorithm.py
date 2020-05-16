from model import Model
from chromosome import Chromosome

import numpy as np
import random
import warnings
import math
import logging
import typing

# lamba = mu * 7


def warning_data_type_check_selection_algorithms(items, probs):
    if type(items) == list:
        items = np.array(items)
    if type(probs) == list:
        probs = np.array(probs)
    if len(probs) != len(items):
        raise ValueError(
            "Length of probs and items must be equal! probs length = {} and items length = {}".format(
                len(probs), len(items)
            )
        )
    if type(probs) != np.ndarray or type(items) != np.ndarray:
        raise ValueError(
            "Type of items and probs must be list or np.array, items type = {} and probs type = {}".format(
                type(items), type(probs)
            )
        )
    if np.min(probs) < 0:
        raise ValueError("Probabilities can not contain negative values")

    if not math.isclose(np.sum(probs), 1):
        warnings.warn(
            "Sum of Probabilities array must be 1 but it is = {}, and we normalize it to reach sum equal 1".format(
                np.sum(probs)
            ),
            stacklevel=4,
        )
        probs = probs / np.sum(probs)
    return items, probs


class EvolutionaryAlgorithm:
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        mu: int,
        y: int,
        max_generation_count: int,
        model: Model,
        window_size: int = 10,
        threshold: float = 0.1,
    ):
        # mu (population size)
        self.m = mu
        # lambda (children size)
        self.y = y
        self.max_generation_count = max_generation_count
        self.average_fitness: typing.List[float] = []

        self.threshold = threshold
        self.window_size = window_size

        self.population = np.array(model.initial_population(mu))
        self.chromosome_type: typing.Type[Chromosome] = model.chromosome_type()

        self.best_chromosome_fitness_in_total = 0
        self.generation_counter = 0

    def run(self) -> Chromosome:
        while True:
            self.average_fitness.append(
                np.average(np.array([p.fitness() for p in self.population]))
            )
            self.logger.info(
                "Generation %d - %f",
                self.generation_counter,
                self.average_fitness[self.generation_counter],
            )
            parents = self.parent_selection()
            children = self.new_children(parents)
            self.population = self.remaining_population_selection(
                self.population, children
            )
            self.generation_counter += 1

            if self.stop_condition():
                break

        return self.get_answer()

    def parent_selection(self):
        fitnesses = np.array([p.fitness() for p in self.population])
        probs = fitnesses / np.sum(fitnesses)

        return self.stochastic_universal_sampling(probs)

    # I have to change it to linear ...
    def stochastic_universal_sampling(self, probs):
        index = np.arange(self.m)
        np.random.shuffle(index)
        items = self.population[index]
        probs = probs[index]
        start_index = np.random.uniform(0, 1 / self.y, 1)
        index_of_choose = np.linspace(start_index, 1, self.y)
        cum_sum = np.cumsum(probs)
        selected_items = []
        items_pointer = 0

        for choice in index_of_choose:
            while cum_sum[items_pointer] < choice:
                if items_pointer == self.m - 1:
                    break
                items_pointer += 1

            selected_items.append(items[items_pointer])

        return np.array(selected_items)

    def new_children(self, parents):
        children = []
        random.shuffle(parents)
        for i in range(0, len(parents) - 1, 2):
            chromosome1, chromosome2 = self.chromosome_type.crossover(
                parents[i], parents[i + 1], 1
            )
            chromosome1.mutate(0.1)
            chromosome2.mutate(0.1)
            children.extend([chromosome1, chromosome2])
            if len(children) >= self.y:
                break

        return children[: self.y]

    def remaining_population_selection(self, previous_population, children):
        items = np.concatenate((previous_population, children))
        fitnesses = np.array([i.fitness() for i in items])
        probs = fitnesses / np.sum(fitnesses)

        return self.q_tournament_selection(items, probs, 2, self.m)

    def q_tournament_selection(self, items, probs, q, n):
        # assert q != 0

        if n == 0:
            return np.array([])

        else:
            items, probs = warning_data_type_check_selection_algorithms(items, probs)
            index = np.arange(len(items))
            np.random.shuffle(index)
            items = items[index]
            probs = probs[index]

            selected_items = []
            len_items = len(items)

            for i in range(n):
                indexes = np.random.choice(np.arange(len_items), q, replace=False)
                selected_items.append(items[indexes[np.argmax(probs[indexes])]])

        return np.array(selected_items)

    def stop_condition(self):
        var = float("inf")
        if len(self.average_fitness) > self.window_size:
            var = np.var(self.average_fitness[-self.window_size :])
        return (
            self.generation_counter > self.max_generation_count or var < self.threshold
        )

    def get_answer(self) -> Chromosome:
        best_phenotype_index = 0
        for i in range(1, len(self.population)):
            if (
                self.population[i].fitness()
                > self.population[best_phenotype_index].fitness()
            ):
                best_phenotype_index = i

        return self.population[best_phenotype_index]
