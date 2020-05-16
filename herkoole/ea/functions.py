import abc
import warnings
import math
import numpy as np


def warning_data_type_check_selection_algorithms(items, probs):
    if type(items) == list:
        items = np.array(items)
    if type(probs) == list:
        probs = np.array(probs)
    if len(probs) != len(items):
        raise ValueError(
            "Length of probs and items must be equal! probs "
            "length = {} and items length = {}".format(len(probs), len(items))
        )
    if type(probs) != np.ndarray or type(items) != np.ndarray:
        raise ValueError(
            "Type of items and probs must be list or np.array,"
            " items type = {} and probs type = {}".format(type(items), type(probs))
        )
    if np.min(probs) < 0:
        raise ValueError("Probabilities can not contain negative values")

    if not math.isclose(np.sum(probs), 1):
        warnings.warn(
            "Sum of Probabilities array must be 1 but it is = {},"
            " and we normalize it to reach sum equal 1".format(np.sum(probs)),
            stacklevel=4,
        )
        probs = probs / np.sum(probs)
    return items, probs


class NextPopulationSelector(abc.ABC):
    def __init__(self):
        self.ea = None

    def __get__(self, obj, objtype):
        self.ea = obj
        return self

    def __call__(self, items, probs):
        items, probs = warning_data_type_check_selection_algorithms(items, probs)
        return self.select(items, probs)

    @abc.abstractmethod
    def select(self, items, probs):
        pass


class ParentSelector(abc.ABC):
    def __init__(self):
        self.ea = None

    def __get__(self, obj, objtype):
        self.ea = obj
        return self

    def __call__(self, probs):
        return self.select(probs)

    @abc.abstractmethod
    def select(self, probs):
        pass


class StochasticUniversalSampling(ParentSelector):
    def select(self, probs):
        index = np.arange(self.ea.m)
        np.random.shuffle(index)
        items = self.ea.population[index]
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
    def __init__(self, q):
        if q == 0:
            raise ValueError("Q must be a possitive number")
        self.q = q
        super().__init__()

    def select(self, items, probs):
        if self.ea.m == 0:
            return np.array([])
        else:
            index = np.arange(len(items))
            np.random.shuffle(index)
            items = items[index]
            probs = probs[index]

            selected_items = []
            len_items = len(items)

            for i in range(self.ea.m):
                indexes = np.random.choice(np.arange(len_items), self.q, replace=False)
                selected_items.append(items[indexes[np.argmax(probs[indexes])]])

        return np.array(selected_items)
