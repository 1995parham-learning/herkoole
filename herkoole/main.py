from ea import EvolutionaryAlgorithm
from knapsack import Model

import typing
import logging
import click


@click.command()
@click.option("--info", "-i", required=True, type=click.Path(exists=True))
@click.option("--iterations", "-t", default=100, type=int)
@click.option("--verbose", "-v", default=False, is_flag=True)
def main(info, iterations, verbose):
    if verbose is True:
        logging.basicConfig(level=logging.INFO)

    with open(info, "r") as f:
        arr = f.readline().split()
        chromosome_length = int(arr[0])
        max_weight = int(arr[1])

        weights: typing.List[int] = []
        values: typing.List[int] = []

        for i in range(chromosome_length):
            value_weight = f.readline().split()
            values.append(int(value_weight[0]))
            weights.append(int(value_weight[1]))

    m = Model(weights, values, max_weight)
    EvolutionaryAlgorithm(10, 20, iterations, m).run()


if __name__ == "__main__":
    main()
