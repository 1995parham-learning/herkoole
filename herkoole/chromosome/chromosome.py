from __future__ import annotations

import abc
import typing


class Chromosome[T](abc.ABC):
    """
    Abstract Chromosome class that must be extended for each problem.
    """

    def __init__(self):
        self.genes: typing.MutableSequence[T] = []

    def __iter__(self) -> typing.Iterator[T]:
        return self.genes.__iter__()

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Chromosome):
            return o.genes == self.genes
        return False

    @abc.abstractmethod
    def fitness(self) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def mutate(self, prob: float):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def crossover(
        cls, parent1: Chromosome, parent2: Chromosome, prob: float,
    ) -> tuple[Chromosome, Chromosome]:
        raise NotImplementedError
