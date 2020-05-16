from .model import Model
from .city import City


def test_initiation():
    cities = [
        City(1, 0, 0),
        City(2, 1, 0),
        City(3, 1, 1),
        City(4, 0, 1),
    ]

    m = Model(cities)
    ch = m.initial_population(1)[0]

    assert len(ch.genes) == len(cities)
    for i in range(len(cities)):
        assert i in ch.genes

    # without mutation
    genes = ch.genes[:]
    ch.mutate(0)
    for i in range(len(cities)):
        assert i in ch.genes
    assert genes == ch.genes

    # with mutation
    genes = ch.genes[:]
    ch.mutate(1)
    for i in range(len(cities)):
        assert i in ch.genes
    diff = 0
    for i, gene in enumerate(genes):
        if ch.genes.index(gene) != i:
            diff += 1
    assert diff == 2
    assert genes != ch.genes
