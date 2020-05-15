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
        res = ""

        for gene in self.genes:
            res += f"{self.model.cities[gene]} -> "

        return res

    def random(self):
        self.genes = [i for i in range(self.model.length)]
        random.shuffle(self.genes)

    def fitness(self) -> float:
        distance = 0

        for i in range(1, self.model.length):
            c1 = self.model.cities[self.genes[i - 1]]
            c2 = self.model.cities[self.genes[i]]
            distance += (c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2

        return distance

    def mutate(self, prob: float):
        rand = random.random()
        if rand < prob:
            random.shuffle(self.genes)

    @classmethod
    def crossover(
        cls, parent1: Chromosome, parent2: Chromosome, prob: float
    ) -> typing.Tuple[chromosome.Chromosome, chromosome.Chromosome]:
        return parent1, parent2
