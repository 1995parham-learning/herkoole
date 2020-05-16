from chromosome import Chromosome

import abc
import typing


class Model(abc.ABC):
    @abc.abstractmethod
    def initial_population(self, mu: int) -> typing.List[Chromosome]:
        pass

    @staticmethod
    @abc.abstractstaticmethod
    def chromosome_type() -> typing.Type[Chromosome]:
        pass
