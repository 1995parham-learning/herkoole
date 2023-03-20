import numpy as np
import numpy.typing as npt

from chromosome import Chromosome
from .evolutionary_algorithm import (
    ParentSelector,
    NextPopulationSelector,
    EvolutionaryAlgorithm,
)


class StochasticUniversalSampling(ParentSelector):
    def select(self, probs: npt.NDArray[np.float64]):
        index = np.arange(self.ea.m)
        np.random.shuffle(index)
        items = np.array(self.ea.population)[index]
        probs = probs[index]
        start_index = np.random.uniform(0, 1 / self.ea.y, 1)
        index_of_choose = np.linspace(start_index, 1, self.ea.y)
        cum_sum = np.cumsum(probs)
        selected_items = []
        items_pointer = 0

        for choice in index_of_choose:
            while cum_sum[items_pointer] < choice:
                if items_pointer == self.ea.m - 1:
                    break
                items_pointer += 1

            selected_items.append(items[items_pointer])

        return np.array(selected_items)


class QTournament(NextPopulationSelector):
    def __init__(self, ea: EvolutionaryAlgorithm, q: float):
        if q == 0:
            raise ValueError("Q must be a possitive number")
        self.q = q
        super().__init__(ea)

    def select(
        self, items: list[Chromosome], probs: npt.NDArray[np.float64]
    ) -> list[Chromosome]:
        if self.ea.m == 0:
            return []

        index = np.arange(len(items))
        np.random.shuffle(index)
        np_items = np.array(items)[index]
        probs = probs[index]

        selected_items = []
        len_items = len(np_items)

        for _ in range(self.ea.m):
            indexes = np.random.choice(
                np.arange(len_items), self.q, replace=False
            )
            selected_items.append(np_items[indexes[np.argmax(probs[indexes])]])

        return list(selected_items)
