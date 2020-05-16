from ea import EvolutionaryAlgorithm
from model import Model
from knapsack import Model as KModel
from tsp import Model as TModel, City

import typing
import logging
import click
import io


def tsp(f: io.TextIOBase) -> Model:
    cities: typing.List[City] = []
    while True:
        line = f.readline()
        if line == "":
            break
        coordinate = line.split()
        identifier = int(coordinate[0])
        x = float(coordinate[1])
        y = float(coordinate[2])
        city = City(identifier, x, y)
        cities.append(city)

    return TModel(cities)


def knapsack(f: io.TextIOBase) -> Model:
    l1 = f.readline().split()
    chromosome_length = int(l1[0])
    max_weight = int(l1[1])

    weights: typing.List[int] = []
    values: typing.List[int] = []

    for i in range(chromosome_length):
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

    m: Model
    with open(info, "r") as f:
        if problem == "knapsack":
            m = knapsack(f)
        elif problem == "tsp":
            m = tsp(f)
        else:
            return

    EvolutionaryAlgorithm(10, 20, iterations, m).run()


if __name__ == "__main__":
    main()
