import typing
import logging
import io
import click

from herkoole.ea import (
    EvolutionaryAlgorithm,
    StochasticUniversalSampling,
    QTournament,
)
from herkoole.model import Model
from herkoole.knapsack import Model as KModel


def knapsack(f: io.TextIOBase) -> Model:
    """
    reads a problem instance from a given file.
    """
    l1 = f.readline().split()
    chromosome_length = int(l1[0])
    max_weight = int(l1[1])

    weights: typing.List[int] = []
    values: typing.List[int] = []

    for _ in range(chromosome_length):
        value_weight = f.readline().split()
        values.append(int(value_weight[0]))
        weights.append(int(value_weight[1]))

    return KModel(weights, values, max_weight)


@click.command()
@click.option("--info", "-i", required=True, type=click.Path(exists=True))
@click.option(
    "--problem",
    "-p",
    default="knapsack",
    type=click.Choice(["tsp", "knapsack"], case_sensitive=False),
)
@click.option("--iterations", "-t", default=100, type=int)
@click.option("--verbose", "-v", default=False, is_flag=True)
def main(info, problem, iterations, verbose):
    if verbose is True:
        logging.basicConfig(level=logging.INFO)

    with open(info, "r", encoding="utf-8") as f:
        if problem == "knapsack":
            m = knapsack(f)
        else:
            return

    print(
        EvolutionaryAlgorithm(
            10,
            20,
            iterations,
            m,
            parent_selector=StochasticUniversalSampling.new(),
            remaining_population_selector=QTournament.new(q=2),
        ).run()
    )


if __name__ == "__main__":
    main()
