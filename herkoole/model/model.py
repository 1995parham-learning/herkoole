import abc
import typing

from herkoole.chromosome import Chromosome


class Model(abc.ABC):
    """
    Model represents the actual problem with its configuration.
    Everything starts here by defining the problem model.
    """

    @abc.abstractmethod
    def initial_population(self, mu: int) -> typing.List[Chromosome]:
        """
        Generate the initial chromosomes.
        """
