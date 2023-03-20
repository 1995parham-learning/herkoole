from __future__ import annotations

import chromosome
import model

import typing
import random


class Model(model.Model):
    def __init__(
        self,
        weights: typing.List[int],
        values: typing.List[int],
        max_weight: int,
    ):
        self.weights = weights
        self.values = values
        self.max_weight = max_weight
        if len(self.weights) != len(self.values):
            raise ValueError("each item must a value and weight")
        self.length: int = len(self.weights)
        Chromosome.model = self

    def initial_population(self, mu: int) -> list[chromosome.Chromosome]:
        population: list[chromosome.Chromosome] = []

        for _ in range(mu):
            chromosome = Chromosome()
            chromosome.random()
            population.append(chromosome)

        return population

    @staticmethod
    def chromosome_type():
        return Chromosome


class Chromosome(chromosome.Chromosome):
    model: Model

    def __init__(self):
        self.genes: typing.List[bool] = []
        if self.model is None:
            raise ValueError("first create problem model")

    def __repr__(self):
        total_weight = 0
        total_value = 0

        for i, gene in enumerate(self.genes):
            if gene is True:
                total_weight += self.model.weights[i]
                total_value += self.model.values[i]
        return f"weight: {total_weight}, value: {total_value} with fitness: {self.fitness()}"

    def random(self):
        for _ in range(self.model.length):
            self.genes.append(True if random.randint(0, 1) == 1 else False)

    def fitness(self) -> float:
        total_weight = 0
        total_value = 0

        for i, gene in enumerate(self.genes):
            if gene is True:
                total_weight += self.model.weights[i]
                total_value += self.model.values[i]

        fitness = total_value

        if total_weight > self.model.max_weight:
            return 1 / fitness

        return fitness

    def mutate(self, prob: float):
        rand = random.random()
        if rand < prob:
            i = random.randrange(self.model.length)
            self.genes[i] = not self.genes[i]

    @classmethod
    def crossover(
        cls, parent1: Chromosome, parent2: Chromosome, prob: float
    ) -> typing.Tuple[chromosome.Chromosome, chromosome.Chromosome]:
        idx = random.randrange(cls.model.length)

        chromosome1, chromosome2 = (
            Chromosome(),
            Chromosome(),
        )
        rand = random.random()
        if rand < prob:
            chromosome1.genes[:idx] = parent1.genes[:idx]
            chromosome1.genes[idx:] = parent2.genes[idx:]
            chromosome2.genes[:idx] = parent2.genes[:idx]
            chromosome2.genes[idx:] = parent1.genes[idx:]
        else:
            chromosome1.genes = parent1.genes[:]
            chromosome2.genes = parent2.genes[:]

        return chromosome1, chromosome2
