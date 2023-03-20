from __future__ import annotations

import abc


class Chromosome(abc.ABC):
    @abc.abstractmethod
    def fitness(self) -> float:
        pass

    @abc.abstractmethod
    def mutate(self, prob: float):
        pass

    @abc.abstractclassmethod
    @classmethod
    def crossover(
        cls, ch1: Chromosome, ch2: Chromosome, prop: float
    ) -> tuple[Chromosome, Chromosome]:
        pass
