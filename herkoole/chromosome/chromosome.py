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

    @abc.abstractmethod
    @classmethod
    def crossover(
        cls, ch1: Chromosome, ch2: Chromosome, prop: float
    ) -> tuple[Chromosome, Chromosome]:
        raise NotImplementedError()
