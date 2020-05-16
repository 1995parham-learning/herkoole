from model import Model
from chromosome import Chromosome

from .functions import (
    QTournament,
    NextPopulationSelector,
    ParentSelector,
    StochasticUniversalSampling,
)

import numpy as np
import random
import logging
import typing


class EvolutionaryAlgorithm:
    logger = logging.getLogger(__name__)

    remaining_population_selector: NextPopulationSelector = QTournament(2)
    parent_selector: ParentSelector = StochasticUniversalSampling()

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

        return self.parent_selector(probs)

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

        return self.remaining_population_selector(items, probs)

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
