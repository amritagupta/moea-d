#!/opt/python/bin/python
"""
A script for solving multi-objective optimization problems using an evolutionary algorithm.
"""
import random, time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
plt.style.use('ggplot')

from utils import *
from subproblem import *
import solution
from parse_lpfile import lp_parser

########## MOEA/D + RUNTIME PARAMETERS ##########
T = 10      # number of neighbors
H = 125
MAXGEN = 20
VERBOSE = True

opt_prob_dir = 'problem_instances/0-1_knapsack/BOKP_lp_format_instances/'
opt_prob_instance = 'kp_20_1'#['kp_20_1', 'kp_80_10']
opt_prob = opt_prob_dir+opt_prob_instance+'.lp'

################ INITIALIZATION ################
EP_history = dict()
n_nondom_pts_history = dict()
# get optimization problem data
prob_data = lp_parser(opt_prob, verbose=False)
n_dvars = prob_data['n_dvars']
n_obj = prob_data['n_obj']
n_constr = prob_data['n_constr']

# initialize moea-d subproblems
lam = generate_lambda_vectors(n_obj, H = H)
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
	if VERBOSE and generation%1 == 0:
		print(generation)
	for i in range(N): # for each subproblem
		tstart = time.time()
		parents = np.random.choice(subproblem_list[i].B,2,replace = False)
		parent1 = subproblem_list[parents[0]].cur_solution
		parent2 = subproblem_list[parents[1]].cur_solution

		offsprings = parent1.crossover_operator(parent2, generation, opt_prob, ideal_Z, subproblem_list[i].lam, verbose=False)         #Genetic Operators
		offspring = offsprings[0].give_the_best_of(offsprings[1], subproblem_list[i].lam, ideal_Z)

		mutated_offspring = offspring.mutation_operator2(0.1, opt_prob, ideal_Z, subproblem_list[i].lam)
		offspring = mutated_offspring
		tend = time.time()
		# print('Creating feasible new offspring took %s seconds'%(tend-tstart))
        # if not mutated_offspring.feasible:
        #     for mc in range(3):
        #         mutated_offspring = repair(mutated_offspring, offspring, opt_prob)
        #         if mutated_offspring.check_feasible(opt_prob):
        #             offspring = mutated_offspring
        #             offspring.objective_val = offspring.evaluate_solution(opt_prob)
        #             break

		ideal_Z = np.minimum(ideal_Z,offspring.objective_val)   # minimizing element-wise

		for j in subproblem_list[i].B:
			subproblem_list[j].cur_solution = subproblem_list[j].cur_solution.give_the_best_of(offspring, subproblem_list[j].lam,ideal_Z)

		EP = remove_newly_dominated_solutions(EP, offspring, objective_sense='min')
		# print('Filtered EP')
		# print [es.objective_val for es in EP]
		EP = add_if_not_dominated(offspring, EP, objective_sense='min')
	# print('Added EP')
	# print [es.objective_val for es in EP]
	# print('---------')
		
	# if generation%1 == 0 and generation > 1:
	# 	Z1 = [es.objective_val[0] for es in EP]
	# 	Z2 = [es.objective_val[1] for es in EP]
	# 	# print Z1
	# 	# print Z2
	# 	x_vector = [es.x for es in EP]
	# 	es_generation = [es.generation for es in EP]
	# 	plt.scatter(Z1, Z2, c=es_generation, cmap=plt.cm.RdYlGn, s=50)

		# plot_z1 = np.arange(min(Z1),max(Z1), 0.1)   #f1value
		# plot_z2 = [1 - np.sqrt(z1val) for z1val in plot_z1]
		# plt.plot(plot_z1, plot_z2)
		# plt.ylim(ymin=0,ymax=6)
		# plt.xlim(xmin=0,xmax=1.2)

		# plt.savefig('figures/generation%s.png'%generation)

	if generation%5 == 0:
		EP_history[generation] = EP
		n_nondom_pts_history[generation] = len(EP)
	# plt.scatter([es.objective_val[0] for es in EP], [es.objective_val[1] for es in EP], s=50)
	# plt.savefig('figures/generation%s.png'%generation)
	# plt.close()

for saved_gen in EP_history:
	plt.scatter([es.objective_val[0] for es in EP_history[saved_gen]], [es.objective_val[1] for es in EP_history[saved_gen]], c=[es.generation for es in EP_history[saved_gen]], cmap = plt.cm.RdYlGn, s=50)
plt.scatter([es.objective_val[0] for es in EP], [es.objective_val[1] for es in EP], marker='+', linewidths=1.5, color='white', s=80)
plt.title(opt_prob_instance, fontsize=14)
plt.savefig('figures/'+opt_prob_instance+'_gen_'+str(MAXGEN)+'_H_'+str(H)+'_approx_frontier.png')
plt.close()

print sorted(n_nondom_pts_history.keys())
plt.plot(sorted(n_nondom_pts_history.keys()), [n_nondom_pts_history[g] for g in sorted(n_nondom_pts_history.keys())])
plt.xlabel('Generation Number')
plt.ylabel('Number of Nondominated Points')
plt.savefig('figures/'+opt_prob_instance+'_gen_'+str(MAXGEN)+'_H_'+str(H)+'_n_ndp_per_gen.png')
plt.close()

# plt.show()