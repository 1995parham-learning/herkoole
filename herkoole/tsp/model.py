from __future__ import annotations

import random

import herkoole.chromosome
import herkoole.model

from .city import City


class Model(herkoole.model.Model):
    def __init__(self, cities: list[City]):
        self.cities = cities
        self.length = len(cities)

    def initial_population(self, mu: int) -> list[herkoole.chromosome.Chromosome]:
        population: list[herkoole.chromosome.Chromosome] = []
        for _ in range(mu):
            chromosome = Chromosome(self)
            chromosome.random()
            population.append(chromosome)
        return population


class Chromosome(herkoole.chromosome.Chromosome[int]):
    def __init__(self, model: Model):
        self.model = model

        super().__init__()

    def __str__(self):
        res = " -> ".join(str(self.model.cities[gene]) for gene in self.genes)

        res += f"\n\tfintess: {self.fitness():.4f}"

        return res

    def random(self):
        self.genes = list(range(self.model.length))
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
        cls,
        parent1: herkoole.chromosome.Chromosome,
        parent2: herkoole.chromosome.Chromosome,
        prob: float,
    ) -> tuple[herkoole.chromosome.Chromosome, herkoole.chromosome.Chromosome]:
        assert isinstance(parent1, Chromosome)
        assert isinstance(parent2, Chromosome)

        rand = random.random()
        if rand >= prob:
            return parent1, parent2

        cycles = [-1] * parent1.model.length
        cycle_no = 1
        cyclestart = (i for i, v in enumerate(cycles) if v < 0)

        for pos in cyclestart:
            while cycles[pos] < 0:
                cycles[pos] = cycle_no
                pos = parent1.genes.index(parent2.genes[pos])

        cycle_no += 1

        child1 = Chromosome(parent1.model)
        child2 = Chromosome(parent1.model)

        child1.genes = [
            parent1.genes[i] if n % 2 else parent2.genes[i]
            for i, n in enumerate(cycles)
        ]
        child2.genes = [
            parent2.genes[i] if n % 2 else parent1.genes[i]
            for i, n in enumerate(cycles)
        ]

        return child1, child2
