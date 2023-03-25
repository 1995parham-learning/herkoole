<h1 align="center"> 🌰 HerKoole 🎒 </h1>

<p align="center">
  <img src="./.github/assets/Hercposter.jpg" alt="Hercposter">
</p>

<p align="center">
  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/1995parham-learning/herkoole/ci.yml?logo=github&style=for-the-badge">
</p>

## Introduction

I want to learn about evolutionary algorithms, so I have created this repository to implement some of its algorithms here.
I am reading the **Introduction to Evolutionary Algorithms** book from Springer.
Repository name comes from [Disney's Hercules](<https://en.wikipedia.org/wiki/Disney's_Hercules_(video_game)>) Video Game.

## Structure

In evolutionary algorithms, we have basic structure to evolve current solution using mutate and crossover
into new solutions to find the optimal one. Each problem needs to have its chromosomes, and each chromosome
represents a solution of that problem.

In `Herkoole` chromosome is an abstract class, and you need to extend it for your solution.
Also, in `Herkoole` there is a class named `Model` which initiates the evolutionary algorithm,
and you also must have a model for your problem.

`Model` stores the problem configuration and creates the first generation with the problem-specific's `Chromosome`.
The `EvolutionaryAlgorithm` class created by your problem's `Model` and solves it. You can customize every aspect of
`EvolutionaryAlgorithm` class with the strategy pattern.

The algorithm stops when it has multiple results that are very similar
or the number of generations passes the threshold.

## Up and Running

### Knapsack

The knapsack problem is the following problem in combinatorial optimization:

> Given a set of items, each with a weight and a value, determine which items to include in the collection
> so that the total weight is less than or equal to a given limit and the total value is as large as possible.

The following files contain a problem instance:

- knapsack_1.txt
- knapsack_2.txt
- knapsack_3.txt
- knapsack_example.txt

Each file has the following format:

```txt
<number of items> <knapsack capcity>
<item value> <item weight>
<item value> <item weight>
...
<item value> <item weight>
```

consider the example problem as follows:

```txt
10 67
505 23
352 26
458 20
220 18
354 32
414 27
498 29
545 26
473 30
543 27
```

Our knapsack has capacity equals to 67, and we can choose between 10 items.
Let's solve this:

```bash
python main.py -p knapsack -i knapsack_example.txt
```

The best solution that is found by our algorithm is (in which we use more probability for mutation):

```
weight: 67, value: 1270 with fitness: 1270
genes:
  - 0: weight: 23, value: 505
  - 3: weight: 18, value: 220
  - 7: weight: 26, value: 545
```

We can run it more to have different solutions:

```
weight: 58, value: 706 with fitness: 706
genes:
  - 1: weight: 26, value: 352
  - 4: weight: 32, value: 354
```

```
weight: 64, value: 1223 with fitness: 1223
genes:
  - 2: weight: 20, value: 458
  - 3: weight: 18, value: 220
  - 7: weight: 26, value: 545
```

```
weight: 48, value: 693 with fitness: 693
genes:
  - 3: weight: 18, value: 220
  - 8: weight: 30, value: 473
```

As you can see all of these solutions are compatible with
the problem constraints, but they are not optimal.

### Travelling salesman problem

The travelling salesman problem (also called the travelling salesperson problem or TSP) asks the following question:

> Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits
> each city exactly once and returns to the origin city?

The following files contain a problem instance:

- tsp_data.txt
- tsp_example.txt

Each file has the following format:

```txt
<city id> <city x coordinate> <city y coordinate>
<city id> <city x coordinate> <city y coordinate>
...
<city id> <city x coordinate> <city y coordinate>
```

consider the example problem as follows:

```txt
1 0 0
2 1 0
3 1 1
4 0 1
```

We have four city place in 1x1 square.
Let's solve this:

```bash
python main.py -p tsp -i tsp_example.txt
```

The solution is:

```
City(identifier=3, x=1.0, y=1.0) -> City(identifier=4, x=0.0, y=1.0) -> City(identifier=1, x=0.0, y=0.0) -> City(identifier=2, x=1.0, y=0.0)
 fintess: 0.3333
```

In which we start by city 2 then continue to city 3 then city 1, and we finish our travel in city 4.
Total distance is equal to:

$$
1 + 1 + 1 = 3
$$
