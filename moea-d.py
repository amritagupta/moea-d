#!/opt/python/bin/python

import random
import numpy as np
from numpy.random import choice
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from g_te import g_te
from lambda_gen import lambda_gen
from lam_nbd import lam_nbd
from SubProblem import *
import Solution
import dominance_check
#PARAMETERS_______________________

T = 10 # number of neighbors
n = 30
m = 2
lam = lambda_gen(m,n)
B = lam_nbd(lam)
N = len(lam)
subproblem_list = []
for i in range(N):
    temp_sol = Solution.Solution(n,['Continuous']*n,i)
    while not temp_sol.feasible:
        temp_sol = Solution.Solution(n, ['Continuous'] * n, i)
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

EP = []
MAXGEN = 250
for generation in range(MAXGEN):
    if generation%20 == 0:
        print(generation)
    for i in range(N): # for each subproblem
        parents = np.random.choice(subproblem_list[i].B,2,replace = False)
        parent1 = subproblem_list[parents[0]].cur_solution
        parent2 = subproblem_list[parents[1]].cur_solution
        offspring = parent1.crossover_operator(parent2)         #Genetic Operators
        #offspring.mutation_operator(0.02, 0.5) # Needs repair kit to be implemented
        #offspring = repair(offspring)

        ideal_Z = np.minimum(ideal_Z,offspring.objective_val)   # minimizing
        for j in subproblem_list[i].B:
            if g_te(offspring,subproblem_list[j].lam, ideal_Z) <= g_te(subproblem_list[j].cur_solution, subproblem_list[j].lam, ideal_Z):
                subproblem_list[j].cur_solution = offspring
        EP = dominance_check.remove_newly_dominated_solutions(EP, offspring, objective_sense='min')
        EP = dominance_check.add_if_not_dominated(offspring, EP, objective_sense='min')

print(EP[0].objective_val[0])

plt.figure()

Z1 = [es.objective_val[0] for es in EP]
Z2 = [es.objective_val[1] for es in EP]
print('hello')
plt.scatter(Z1, Z2)
print(';)')
plt.show()