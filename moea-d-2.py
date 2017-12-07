#!/opt/python/bin/python
"""
A script for solving multi-objective optimization problems using an evolutionary algorithm.
"""
import random
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from utils import *
from subproblem import *
import solution
from parse_lpfile import lp_parser

########## MOEA/D + RUNTIME PARAMETERS ##########
T = 10      # number of neighbors
MAXGEN = 500
VERBOSE = True

opt_prob = 'problem_instances/0-1_knapsack/BOKP_lp_format_instances/kp_20_1.lp'

################ INITIALIZATION ################
# get optimization problem data
prob_data = lp_parser(opt_prob, verbose=False)
n_dvars = prob_data['n_dvars']
n_obj = prob_data['n_obj']
n_constr = prob_data['n_constr']

# initialize moea-d subproblems
lam = generate_lambda_vectors(n_obj)
N = len(lam) # number of subproblems
B = get_lambda_neighborhoods(lam)
subproblem_list = []
for i in range(N):
	temp_sol = solution.Solution(i, opt_prob)
	while not temp_sol.feasible:
		temp_sol = solution.Solution(i, opt_prob)
	temp_sub = SubProblem(i,lam[i,:],B[i,:], temp_sol)
	subproblem_list.append(temp_sub)
if VERBOSE:
	print('Generated an initial set of randomly generated feasible solutions.')

list_of_solution = [subprob.cur_solution for subprob in subproblem_list]
solution_objs = [subprob.cur_solution.objective_val for subprob in subproblem_list]
ideal_Z  = [None] * n_obj
for sol in list_of_solution:
    for obj_dim in range(len(sol.objective_val)):
        if ideal_Z[obj_dim] == None:
            ideal_Z[obj_dim] = sol.objective_val[obj_dim]
        if sol.objective_val[obj_dim] < ideal_Z[obj_dim]:   #minimizing
            ideal_Z[obj_dim] = sol.objective_val[obj_dim]

########## BEGIN EVOLUTIONARY ALGORITHM ##########

EP = []
for generation in range(MAXGEN):
    if VERBOSE and generation%20 == 0:
        print(generation)
    for i in range(N): # for each subproblem
        parents = np.random.choice(subproblem_list[i].B,2,replace = False)
        parent1 = subproblem_list[parents[0]].cur_solution
        parent2 = subproblem_list[parents[1]].cur_solution

        offsprings = parent1.crossover_operator(parent2, generation, optimization_problem)         #Genetic Operators
        offspring = offsprings[0].give_the_best_of(offsprings[1], subproblem_list[i].lam, ideal_Z)

        mutated_offspring = offspring.mutation_operator2(0.1, optimization_problem)

        if not mutated_offspring.feasible:
            for mc in range(3):
                mutated_offspring = repair(mutated_offspring, offspring, optimization_problem)
                if mutated_offspring.check_feasible(optimization_problem):
                    offspring = mutated_offspring
                    offspring.objective_val = offspring.evaluate_solution(optimization_problem)
                    break

        ideal_Z = np.minimum(ideal_Z,offspring.objective_val)   # minimizing element-wise

        for j in subproblem_list[i].B:
            subproblem_list[j].cur_solution = subproblem_list[j].cur_solution.give_the_best_of(offspring,
                                                                                               subproblem_list[j].lam,
                                                                                               ideal_Z)
        EP = remove_newly_dominated_solutions(EP, offspring, objective_sense='min')
        EP = add_if_not_dominated(offspring, EP, objective_sense='min')