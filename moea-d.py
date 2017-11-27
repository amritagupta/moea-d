#!/opt/python/bin/python

"""
A script for solving multi-objective optimization problems using an evolutionary algorithm.
Does not currently support reading LP files.
"""

import random
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from utils import *
from subproblem import *
import solution


########## MOEA/D + RUNTIME PARAMETERS ##########
T = 10      # number of neighbors
n = 30      # ??
m = 2       # number of objectives
MAXGEN = 500
verbose = True

################ INITIALIZATION ################
lam = generate_lambda_vectors(m)
B = get_lambda_neighborhoods(lam)
N = len(lam) # number of subproblems
subproblem_list = []
for i in range(N):
    temp_sol = solution.Solution(n,['Continuous']*n,i)
    while not temp_sol.feasible:
        temp_sol = solution.Solution(n, ['Continuous'] * n, i)
    temp_sub = SubProblem(i,lam[i,:],B[i,:],temp_sol)
    subproblem_list.append(temp_sub)

list_of_solution = [subprob.cur_solution for subprob in subproblem_list]
ideal_Z  = [None] * m
for sol in list_of_solution:
    for obj_dim in range(len(sol.objective_val)):
        if ideal_Z[obj_dim] == None:
            ideal_Z[obj_dim] = sol.objective_val[obj_dim]
        if sol.objective_val[obj_dim] < ideal_Z[obj_dim]:   #minimizing
            ideal_Z[obj_dim] = sol.objective_val[obj_dim]

########## BEGIN EVOLUTIONARY ALGORITHM ##########

EP = []
for generation in range(MAXGEN):
    if verbose and generation%20 == 0:
        print(generation)
    for i in range(N): # for each subproblem
        parents = np.random.choice(subproblem_list[i].B,2,replace = False)
        parent1 = subproblem_list[parents[0]].cur_solution
        parent2 = subproblem_list[parents[1]].cur_solution

        offsprings = parent1.crossover_operator(parent2, generation)         #Genetic Operators
        offspring = offsprings[0].give_the_best_of(offsprings[1], subproblem_list[i].lam, ideal_Z)

        offspring.mutation_operator2(0.1)
        # check feasibility
        #offspring = repair(offspring)

        ideal_Z = np.minimum(ideal_Z,offspring.objective_val)   # minimizing element-wise
        for j in subproblem_list[i].B:
            subproblem_list[j].cur_solution = subproblem_list[j].cur_solution.give_the_best_of(offspring,
                                                                                               subproblem_list[j].lam,
                                                                                               ideal_Z)
        EP = remove_newly_dominated_solutions(EP, offspring, objective_sense='min')
        EP = add_if_not_dominated(offspring, EP, objective_sense='min')

    if generation%50 == 0:
        Z1 = [es.objective_val[0] for es in EP]
        Z2 = [es.objective_val[1] for es in EP]
        x_vector = [es.x for es in EP]
        es_generation = [es.generation for es in EP]
        plt.scatter(Z1, Z2, c=es_generation, cmap=plt.cm.RdYlGn, s=50)

        plot_z1 = np.arange(min(Z1),max(Z1), 0.1)   #f1value
        plot_z2 = [1 - np.sqrt(z1val) for z1val in plot_z1]
        plt.plot(plot_z1, plot_z2)
        plt.ylim(ymax=6)
        plt.xlim(xmax=1.2)

        plt.savefig('generation%s.png'%generation)
