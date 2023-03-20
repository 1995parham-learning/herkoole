<h1 align="center"> 🌰 HerKoole 🎒 </h1>

<p align="center">
  <img src="./.github/assets/Hercposter.jpg" alt="Hercposter">
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
Also, in `Herkoole` there is a class named Model which initiates the evolutionary algorithm,
and you also must have a model for your problem.

## Up and Running

```bash
python3 herkoole/main.py -v --info tsp_example.txt -t 3000 -p tsp
```

```bash
python3 herkoole/main.py -v --info knapsack_example.txt -t 3000 -p knapsack
```
