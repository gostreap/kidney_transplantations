# Pairing mechanisms for kidney transplants
My solution to a mini-project of the course INF421 of the Ecole Polytechnique.

## Install
Let's create a virtual environment for python and install the necessary libraries.

The only library needed to run the algorithms is `pulp`. The others are useful for data generation and for graph visualization.
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Location of the algorithms

### Question 1

The direct donation algorithm is implemented in the file `src/direct_donation.py`.

### Question 2

The greedy matching  algorithm is implemented in the file `src/greedy_matching.py`.

### Question 4

The cycles and chains matching algorithm is implemented in the file `src/cycles_and_chains_matching.py`.

### Question 9

The algorithm that lists all minimal infeasible paths in a directed graph is implemented in the file `src/minimal_infeasible_paths.py`.

### Question 11 

The algorithm that solves the ILP using Branch-and-Bound is implemented in the file `src/ilp.py`.

## Benchmark and utils for ILP

The results of the benchmarks for questions 9 and 12 were obtained using the functions in the file `src/benchmark.py`.

A number of functions useful for problem generation and visualization are in the `src/ilp_utils.py` file.

However, these files were not written to be read by the professor.

## Simulation / Question 13

The data generation and the simulation code are in the file `src/simulation.py`.

This file was also not written to be read by the professor.