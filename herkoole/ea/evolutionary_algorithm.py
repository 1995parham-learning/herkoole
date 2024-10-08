"""
Evolutionary algorithm core types and selection algorithms.
"""

from __future__ import annotations

import abc
import logging
import random
import typing

import numpy as np
import numpy.typing as npt

if typing.TYPE_CHECKING:
    from herkoole.chromosome import Chromosome
    from herkoole.model import Model


class NextPopulationSelector(abc.ABC):
    """
    With NextPopulationSelector you can customize the evolutionary
    algorithm population selection phase.
    """

    def __init__(self, ea: EvolutionaryAlgorithm) -> None:
        self.ea = ea

    def __call__(
        self,
        items: list[Chromosome],
        probs: npt.NDArray[np.float64],
    ) -> list[Chromosome]:
        return self.select(items, probs)

    @classmethod
    def new(
        cls,
        *args,  # noqa: ANN002
        **kwargs,  # noqa: ANN003
    ) -> typing.Callable[[EvolutionaryAlgorithm], NextPopulationSelector]:
        """
        We need to instantiate the selector in EvolutionaryAlgorithm class,
        and pass the instance to. using this function users can customize
        the parameters and put only the instantiation
        for EvolutionaryAlgorithm class.
        """

        def _new(ea: EvolutionaryAlgorithm) -> NextPopulationSelector:
            return cls(ea, *args, **kwargs)

        return _new

    @abc.abstractmethod
    def select(
        self,
        items: list[Chromosome],
        probs: npt.NDArray[np.float64],
    ) -> list[Chromosome]:
        pass


class ParentSelector(abc.ABC):
    """
    With ParentSelector you can customize the evolutionary
    algorithm parent selection phase.
    """

    def __init__(self, ea: EvolutionaryAlgorithm) -> None:
        self.ea = ea

    def __call__(self, probs: npt.NDArray[np.float64]) -> list[Chromosome]:
        return self.select(probs)

    @classmethod
    def new(
        cls,
        *args,  # noqa: ANN002
        **kwargs,  # noqa: ANN003
    ) -> typing.Callable[[EvolutionaryAlgorithm], ParentSelector]:
        def _new(ea: EvolutionaryAlgorithm) -> ParentSelector:
            return cls(ea, *args, **kwargs)

        return _new

    @abc.abstractmethod
    def select(self, probs: npt.NDArray[np.float64]) -> list[Chromosome]:
        pass


class EvolutionaryAlgorithm:
    """
    Evolutionary algorithm base class which is the same between problems.
    """

    logger = logging.getLogger(__name__)

    def __init__(  # noqa: PLR0913
        self,
        mu: int,
        y: int,
        max_generation_count: int,
        model: Model,
        parent_selector: typing.Callable[[EvolutionaryAlgorithm], ParentSelector],
        remaining_population_selector: typing.Callable[
            [EvolutionaryAlgorithm],
            NextPopulationSelector,
        ],
        window_size: int = 10,
        threshold: float = 0.1,
        mutation_propability: float = 0.1,
        crossover_propability: float = 1,
    ) -> None:
        # mu (population size)
        self.m = mu
        # lambda (children size)
        self.y = y
        self.max_generation_count = max_generation_count
        self.average_fitness: list[float] = []

        self.threshold = threshold
        self.window_size = window_size

        self.population: list[Chromosome] = model.initial_population(mu)

        self.best_chromosome_fitness_in_total = 0
        self.generation_counter = 0

        self.parent_selector = parent_selector(self)
        self.remaining_population_selector = remaining_population_selector(self)

        self.mutation_propabiity = mutation_propability
        self.crossover_propability = crossover_propability

    def run(self) -> Chromosome:
        while True:
            self.average_fitness.append(
                float(np.average(np.array([p.fitness() for p in self.population]))),
            )
            self.logger.info(
                "Generation %d - %f",
                self.generation_counter,
                self.average_fitness[self.generation_counter],
            )
            parents = self.parent_selection()
            children = self.new_children(parents)
            self.population = self.remaining_population_selection(
                self.population,
                children,
            )
            self.generation_counter += 1

            if self.stop_condition():
                break

        return self.get_answer()

    def parent_selection(self) -> list[Chromosome]:
        fitnesses = np.array([p.fitness() for p in self.population])
        probs = fitnesses / np.sum(fitnesses)

        return self.parent_selector(probs)

    def new_children(self, parents: list[Chromosome]) -> list[Chromosome]:
        children: list[Chromosome] = []

        random.shuffle(parents)

        chromosome_type: type[Chromosome] = type(parents[0])

        for i in range(0, len(parents) - 1, 2):
            chromosome1, chromosome2 = chromosome_type.crossover(
                parents[i],
                parents[i + 1],
                self.crossover_propability,
            )
            chromosome1.mutate(self.mutation_propabiity)
            chromosome2.mutate(self.mutation_propabiity)
            children.extend([chromosome1, chromosome2])
            if len(children) >= self.y:
                break

        return children[: self.y]

    def remaining_population_selection(
        self,
        previous_population: list[Chromosome],
        children: list[Chromosome],
    ) -> list[Chromosome]:
        items = [*previous_population, *children]
        fitnesses = np.array([i.fitness() for i in items])
        probs = fitnesses / np.sum(fitnesses)

        return self.remaining_population_selector(items, probs)

    def stop_condition(self) -> bool:
        var = float("inf")
        if len(self.average_fitness) > self.window_size:
            var = float(np.var(np.array(self.average_fitness[-self.window_size :])))
        return (
            self.generation_counter > self.max_generation_count or var < self.threshold
        )

    def get_answer(self) -> Chromosome:
        return max(self.population, key=lambda p: p.fitness())
