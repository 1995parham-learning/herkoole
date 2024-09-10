"""
Knapsack problem is:

Given a set of items, each with a weight and a value, determine
which items to include in the collection so that the total weight
is less than or equal to a given limit
and the total value is as large as possible
"""

from __future__ import annotations

import random

import herkoole.chromosome
import herkoole.model


class Model(herkoole.model.Model):
    def __init__(
        self,
        weights: list[int],
        values: list[int],
        max_weight: int,
    ) -> None:
        self.weights = weights
        self.values = values
        self.max_weight = max_weight
        if len(self.weights) != len(self.values):
            raise ValueError
        self.length: int = len(self.weights)

    def initial_population(self, mu: int) -> list[herkoole.chromosome.Chromosome]:
        population: list[herkoole.chromosome.Chromosome] = []

        for _ in range(mu):
            chromosome = Chromosome(self)
            chromosome.random()
            population.append(chromosome)

        return population


class Chromosome(herkoole.chromosome.Chromosome[bool]):
    """
    Chromosome represents a one solution for knapsack problem which shows
    an item selection. Each gens coresponds into an item which is picked
    or not.
    """

    def __init__(self, model: Model) -> None:
        self.model = model
        super().__init__()

    def __str__(self) -> str:
        total_weight = 0
        total_value = 0

        for i, gene in enumerate(self.genes):
            if gene is True:
                total_weight += self.model.weights[i]
                total_value += self.model.values[i]  # noqa: PD011

        genes = "\n".join(
            f"\t - {i}: weight: {self.model.weights[i]}"
            f", value: {self.model.values[i]}"  # noqa: PD011
            for i, gene in enumerate(self.genes)
            if gene is True
        )
        return (
            f"weight: {total_weight}, "
            f"value: {total_value} with fitness: {self.fitness()}\n"
            f"genes:\n{genes}"
        )

    def random(self) -> None:
        """
        set values for gens randomly
        """
        for _ in range(self.model.length):
            self.genes.append(random.randint(0, 1) == 1)

    def fitness(self) -> float:
        total_weight = 0
        total_value = 0

        for i, gene in enumerate(self.genes):
            if gene is True:
                total_weight += self.model.weights[i]
                total_value += self.model.values[i]  # noqa: PD011

        fitness = total_value

        # reduce the fitnees to make sure we don't passes
        # the constraints.
        if total_weight > self.model.max_weight:
            return 1 / fitness

        return fitness

    def mutate(self, prob: float) -> None:
        rand = random.random()
        if rand < prob:
            i = random.randrange(self.model.length)
            self.genes[i] = not self.genes[i]

    @classmethod
    def crossover(
        cls,
        parent1: herkoole.chromosome.Chromosome,
        parent2: herkoole.chromosome.Chromosome,
        prob: float,
    ) -> tuple[herkoole.chromosome.Chromosome, herkoole.chromosome.Chromosome]:
        if not isinstance(parent1, cls) or not isinstance(parent2, cls):
            raise TypeError

        idx = random.randrange(parent1.model.length)

        chromosome1, chromosome2 = (
            Chromosome(parent1.model),
            Chromosome(parent2.model),
        )

        rand = random.random()
        if rand < prob:
            chromosome1.genes[:idx] = parent1.genes[:idx]
            chromosome1.genes[idx:] = parent2.genes[idx:]
            chromosome2.genes[:idx] = parent2.genes[:idx]
            chromosome2.genes[idx:] = parent1.genes[idx:]
        else:
            chromosome1.genes[:] = parent1.genes[:]
            chromosome2.genes[:] = parent2.genes[:]

        return chromosome1, chromosome2
