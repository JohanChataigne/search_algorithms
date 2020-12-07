# Genetic Algorithms Project
Authors: [Germon Paul](https://github.com/pgermon) and [Chataigner Johan](https://github.com/JohanChataigne)

## Introduction

![Program demo with test projects](images/screen.png)

This project tries to compute an optimal schedule given a list of projects with their duration and deadline.

To do so, the program uses a genetic algorithm.

One invidual, called **Chromosome**, represents a list of projects in a certain order *i.e* a solution to the schedule problem.

The **reproduction** mechanism between two individuals works this way:
_ two children are created
_ each one inherits from the whole solution of one parent (one different parent per child)
_ for each child, one project is forced to its position in the solution of the parent it didn't inherit from.

A **mutation** correspond to swapping 2 projects in the mutant individual's solution.

To continue, for **one generation** in a population, the next generation is created by keeping the 4 best individuals of the previous one and then performing random reproductions between the old generation's individuals.

To finish, the solution answered by the program for your custom problem is the best found among multiple populations after multiple generations. These values can be changed in the `Configuration()` class, as well as the mutation rate.

## Run commands
-`make` to run the program with your custom projects
-`make test` to run it on test projects


