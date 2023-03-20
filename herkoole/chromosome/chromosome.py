from __future__ import annotations

import abc


class Chromosome(abc.ABC):
    """
    Abstract Chromosome class that must be extended for each problem.
    """

    @abc.abstractmethod
    def fitness(self) -> float:
        raise NotImplementedError()

    @abc.abstractmethod
    def mutate(self, prob: float):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def crossover(
        cls, parent1: Chromosome, parent2: Chromosome, prob: float
    ) -> tuple[Chromosome, Chromosome]:
        raise NotImplementedError()
