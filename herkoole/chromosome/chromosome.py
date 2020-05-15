from __future__ import annotations

import abc
import typing


class Chromosome(abc.ABC):
    @abc.abstractmethod
    def fitness(self) -> float:
        pass

    @abc.abstractmethod
    def mutate(self, prob: float):
        pass

    @classmethod
    @abc.abstractclassmethod
    def crossover(cls, ch1, ch2, prop: float) -> typing.Tuple[Chromosome, Chromosome]:
        pass
