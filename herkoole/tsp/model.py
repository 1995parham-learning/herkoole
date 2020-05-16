from __future__ import annotations

from .city import City

import chromosome
import model

import typing
import random


class Model(model.Model):
    def __init__(self, cities: typing.List[City]):
        self.cities = cities
        self.length = len(cities)
        Chromosome.model = self

    def initial_population(self, mu: int) -> typing.List[chromosome.Chromosome]:
        population: typing.List[chromosome.Chromosome] = []
        for i in range(mu):
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
        self.genes: typing.List[int] = []
        if self.model is None:
            raise ValueError("first create problem model")

    def __repr__(self):
        res = " -> ".join(repr(self.model.cities[gene]) for gene in self.genes)

        res += f"\t fintess: {self.fitness():.4f}"

        return res

    def random(self):
        self.genes = [i for i in range(self.model.length)]
        random.shuffle(self.genes)

    def fitness(self) -> float:
        distance = 0.0

        for i in range(1, self.model.length):
            c1 = self.model.cities[self.genes[i - 1]]
            c2 = self.model.cities[self.genes[i]]
            distance += (c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2

        return 1 / distance

    def mutate(self, prob: float):
        rand = random.random()
        if rand < prob:
            i, j = random.sample(range(self.model.length), 2)
            self.genes[i], self.genes[j] = self.genes[j], self.genes[i]

    @classmethod
    def crossover(
        cls, parent1: Chromosome, parent2: Chromosome, prob: float
    ) -> typing.Tuple[chromosome.Chromosome, chromosome.Chromosome]:
        rand = random.random()
        if rand >= prob:
            return parent1, parent2

        cycles = [-1] * cls.model.length
        cycle_no = 1
        cyclestart = (i for i, v in enumerate(cycles) if v < 0)

        for pos in cyclestart:
            while cycles[pos] < 0:
                cycles[pos] = cycle_no
                pos = parent1.genes.index(parent2.genes[pos])

        cycle_no += 1

        child1 = Chromosome()
        child2 = Chromosome()

        child1.genes = [
            parent1.genes[i] if n % 2 else parent2.genes[i]
            for i, n in enumerate(cycles)
        ]
        child2.genes = [
            parent2.genes[i] if n % 2 else parent1.genes[i]
            for i, n in enumerate(cycles)
        ]

        return child1, child2
