# HerKoole
[![Drone (cloud)](https://img.shields.io/drone/build/1995parham/HerKoole.svg?style=flat-square)](https://cloud.drone.io/1995parham/HerKoole)

## Introduction
I want to learn about evolutionary algorithms so I have created this repository to implement some of the algorithms here.
I am reading the **Introduction to Evolutionary Algorithms** book from Springer.
Repository name comes from [Disney's Hercules](https://en.wikipedia.org/wiki/Disney's_Hercules_(video_game)) Video Game.

## Structure
I am trying to create a generic structure for evolutionary algorithms, but I am not sure this structure is good or useful.

## Up and Running

```sh
python3 herkoole/main.py -v --info tsp_example.txt -t 3000 -p tsp
```

```sh
python3 herkoole/main.py -v --info knapsack_example.txt -t 3000 -p knapsack
```
