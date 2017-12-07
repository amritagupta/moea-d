#!/usr/bin/python
"""
This module defines objects related to the population in the MOEA/D genetic algorithm.
"""
import numpy as np
import random
import utils as utils
# from read_input import read_input
from parse_lpfile import lp_parser

class Solution(object):
	"""
	A single instance of a Solution has the following properties:
	Attributes:
		x: The value in each dimension of the solution.
		n_dim: The number of dimensions in the solution.
		num_type: The numeric type of each dimension.
		generation: The generation number in which it was created.
		subproblem: The subproblem number to which it is a solution.
		feasible: Whether or not the solution is feasible.
		objective_val: The value of the solution in objective space.
	"""
	def __init__(self, subproblem, optimization_problem):
		"""
		Construct a new 'Solution' instance by random generation.
		:param n_dim: The number of dimensions the solution has.
		:param v_type: The numeric type of each dimension.
		:param subproblem: The subproblem number to which it is a solution.
		"""
		super(Solution, self).__init__()
		self.generation = 1
		self.subproblem = subproblem

		if optimization_problem == 'ZDT1':
			self.n_dim = 30
			lb = [0]*self.n_dim
			ub = [1]*self.n_dim
			self.x = np.random.uniform(size=(1, self.n_dim))
			self.feasible = self.check_feasible(optimization_problem) # should be no need to repair ZDT1 with random.uniform since x\in[0,1] is the only constraint
			if not self.feasible:
				raise ValueError('The initialized solution to ZDT1 is not feasible.')
			self.objective_val = self.evaluate_solution(optimization_problem)
			self.v_type = ['C']*self.n_dim

		else:
			prob_data = lp_parser(optimization_problem, verbose=False)
			self.n_dim = prob_data['n_dvars']
			lb = prob_data['lb']
			ub = prob_data['ub']
			self.v_type = prob_data['vartype']
			self.x = np.zeros([1, self.n_dim])
			self.feasible = False
			# generate a random solution
			for i in range(self.n_dim):
				if self.v_type[i] == 'C': # continuous
					self.x[0,i] = np.random.uniform(low=lb[i,0], high=ub[i,0])
				elif self.v_type[i] == 'B': # binary
					self.x[0,i] = np.random.randint(low=0, high=2)
				else:
					raise ValueError('Need to check that vartype is integer and not binary')
					self.x[0,i] = np.random.randint(low=lb[i,0], high=ub[i,0]+1)
			# check constraint feasibility
			self.feasible = self.check_feasible(optimization_problem)
			# repair if necessary
			while not self.feasible:
				self.repair_step(optimization_problem)
				self.feasible = self.check_feasible(optimization_problem)
			self.objective_val = self.evaluate_solution(optimization_problem)





			# opt_params = read_input(optimization_problem)
			# lb = opt_params[3]
			# self.n_dim = len(lb)
		
		
		# self.feasible = False
		# self.objective_val = None
		# self.x = [None]*self.n_dim
		# if optimization_problem == 'ZDT1':
		# 	self.num_type = [0]*self.n_dim
		# else:
		# 	opt_params = read_input(optimization_problem)
		# 	self.num_type = opt_params[5]

		# if not len(self.num_type) == self.n_dim:
		# 	raise ValueError('The number of dimensions does not match the length of the numeric type specification.')

		# for i in range(self.n_dim):
		# 	if self.num_type[i] == 1:
		# 		# generate 0 or 1
		# 		self.x[i] = np.random.randint(2)
		# 	elif self.num_type[i] == 0:
		# 		# generate random real number between 0 and 1
		# 		self.x[i] = np.random.uniform()

		# self.objective_val = self.evaluate_solution(optimization_problem)
		# self.feasible = self.check_feasible(optimization_problem)


	def check_feasible(self, optimization_problem):
		"""
		Check that a solution x satisfies constraints in the optimization_problem.
		:param optimization_problem: For now, only evaluates ZDT1
		"""
		any_constraint_violated = False
		solution_feasible = True

		if optimization_problem == 'ZDT1':
			for i in range(self.n_dim):
				if self.x[0,i] > 1 or self.x[i] < 0:
					any_constraint_violated = True
					break
		else:
			prob_data = lp_parser(optimization_problem, verbose=False)
			constr_coeff = prob_data['constr_coeff']
			constr_RHS = prob_data['constr_RHS']
			constr_sense = prob_data['constr_sense']
			lb = prob_data['lb']
			ub = prob_data['ub']
			v_type = prob_data['vartype']

			# First, check that all variables within bounds
			for i in range(len(self.x)):
				if self.x[0,i] > ub[i,0] or self.x[0,i] < lb[i,0]:
					any_constraint_violated = True
					break
			
			# Next, check that Ax {<=, >=, ==} b
			for c in range(prob_data['n_constr']):
				Ax = np.dot(constr_coeff[c,:], self.x[0])
				if constr_sense[c] == '<' and Ax > constr_RHS[c,0]:
					any_constraint_violated = True
					break
				elif constr_sense[c] == '>' and Ax < constr_RHS[c,0]:
					any_constraint_violated = True
					break
				elif constr_sense[c] == '=' and Ax != constr_RHS[c,0]:
					any_constraint_violated = True
					raise ValueError('Equality constraint violated. Need to implement a sensible fix for this case.')
					break

			# Finally, check if the variable types are correct
			for i in range(len(self.x)):
				if v_type[i] == 'B' and not (self.x[0,i] in [0, 1, float(0), float(1)]):
					any_constraint_violated = True
					break

		if any_constraint_violated:
			solution_feasible = False
		else:
			solution_feasible = True

		return solution_feasible

	def repair_step(self, optimization_problem):
		prob_data = lp_parser(optimization_problem, verbose=False)
		constr_coeff = prob_data['constr_coeff']
		constr_RHS = prob_data['constr_coeff']
		constr_sense = prob_data['constr_sense']
		lb = prob_data['lb']
		ub = prob_data['ub']
		v_type = prob_data['vartype']

		# Repair bound violations
		for i in range(len(self.x)):
			if self.x[0,i] > ub[i,0] or self.x[0,i] < lb[i,0]:
				print('BOUND VIOLATION FOUND')
				if v_type[i] == 'C':
					self.x[0,i] -= np.random.uniform(low=lb[i,0], high=ub[i,0])
		if self.check_feasible(optimization_problem):
			return self

		# Repair constraint violations
		for c in range(prob_data['n_constr']):
			Ax = np.dot(constr_coeff[c,:], self.x[0])
			if constr_sense[c] == '<' and Ax > constr_RHS[c,0]:
				# randomly select a variable in this constraint expression and decrease/flip bit to 0
				nonzero_coeffs = [i for i, e in enumerate(constr_coeff[c,:]) if e != 0]
				change_idx = np.random.choice(nonzero_coeffs)
				if v_type[change_idx] == 'B':
					self.x[0,change_idx] = 0
				elif v_type[change_idx] == 'C':
					self.x[0,change_idx] -= np.random.uniform(low=0, high=(self.x[0,change_idx] - lb[change_idx]))
			elif constr_sense[c] == '>' and Ax < constr_RHS[c,0]:
				# randomly select a variable in this constraint expression and increase/flip bit to 1
				nonzero_coeffs = [i for i, e in enumerate(constr_coeff[c,:]) if e != 0]
				change_idx = np.random.choice(nonzero_coeffs)
				if v_type[change_idx] == 'B':
					self.x[0,change_idx] = 1
				elif v_type[change_idx] == 'C':
					self.x[0,change_idx] += np.random.uniform(low=0, high=(ub[change_idx] - self.x[0,change_idx]))
			elif constr_sense[c] == '=' and Ax != constr_RHS[c]:
				raise ValueError('Equality constraint violated. Need to implement a sensible fix for this case.')
		return self



	def evaluate_solution(self, optimization_problem):
		"""
		Evaluate a solution x to get a list of objective values.
		:param optimization_problem: For now, only evaluates ZDT1
		"""
		if optimization_problem == 'ZDT1':
			n = len(self.x)
			if not n == 30:
				raise ValueError('The solution needs to have dim 30 for the ZDT1 test instance.')

			f1 = self.x[0]
			g = 1 + 9*(sum(self.x[j] for j in range(1,n)))/(n-1)
			f2 = g*(1 - np.sqrt(f1/g))

			return [f1, f2]
		else:
			prob_data = lp_parser(optimization_problem, verbose=False)
			objective_coefficients = prob_data['obj_coeff']
			f = np.zeros([1, prob_data['n_obj']])
			for o in range(prob_data['n_obj']):
				f[0,o] = np.dot(objective_coefficients[o,:], self.x[0])

			return f[0]


	

	def crossover_operator(self, solution2, generation, optimization_problem):
		"""
		Do cross over operations on 2 parents, choosing the best child with the g function
		"""
		crossover_point = random.choice(range(1, self.n_dim - 1))

		# new_solution1 = Solution(self.subproblem, optimization_problem)
		new_solution1 = self
		# new_solution2 = Solution(self.subproblem, optimization_problem)
		new_solution2 = solution2
		new_solution1.generation = generation
		new_solution2.generation = generation

		for dimension in range(0, self.n_dim - 1):
			if dimension < crossover_point:
				new_solution1.x[dimension] = self.x[dimension]
				new_solution2.x[dimension] = solution2.x[dimension]
			elif dimension >= crossover_point:
				new_solution1.x[dimension] = solution2.x[dimension]
				new_solution2.x[dimension] = self.x[dimension]

		new_solution1.objective_val = new_solution1.evaluate_solution(optimization_problem)
		new_solution2.objective_val = new_solution2.evaluate_solution(optimization_problem)
		new_solution1.feasible = new_solution1.check_feasible(optimization_problem)
		new_solution2.feasible = new_solution2.check_feasible(optimization_problem)
		# One should never have to choose between his child..
		#child_choice = random.choice(range(1,2))
		#if child_choice == 1:
		#	child = new_solution1
		#elif child_choice == 2:
		#	child = new_solution2

		offsprings = [new_solution1, new_solution2]

		return offsprings

	def give_the_best_of(self, solution2, lambda_sub, ideal_z):
		"""
		Compare 2 solutions wiht the gte function and return the ebst (the lowest)
		"""
		grade1 = utils.g_te(self,lambda_sub, ideal_z)
		grade2 = utils.g_te(solution2,lambda_sub, ideal_z)

		if grade1 < grade2:
			best = self

		else:
			best = solution2

		return best

	def mutation_operator1(self):
		"""
		Do mutation operation on a solution
		"""
		evolution = self
		mutated_dimension = np.random.randint(1, self.n_dim - 1)

		if self.num_type[mutated_dimension] == 0: # Continuous
			evolution.x[mutated_dimension] = self.x[mutated_dimension] + np.random.normal(0, self.x[mutated_dimension]^2 + 1)

		elif self.num_type[mutated_dimension] == 1: # Binary
			if self.x[mutated_dimension] == 1:
				evolution.x[mutated_dimension] = 0
			elif self.x[mutated_dimension] == 0:
				evolution.x[mutated_dimension] = 1

		return evolution

	def mutation_operator2(self, frequency_of_change, optimization_problem):
		"""
		Do mutation operation on a solution
		"""
		evolution = self

		for dimension in range(0, self.n_dim):
			if self.num_type[dimension] == 0: # Continuous
				change = np.random.binomial(1, frequency_of_change)
				if change == 1:
					#print(self.x[dimension])
					evolution.x[dimension] = np.random.uniform(0, 1) #evolution.x[dimension] + np.random.normal(0, (self.x[dimension]**2)/100)#

			elif self.num_type[dimension] == 1: # Binary
				change = np.random.binomial(1, frequency_of_change)
				if change == 1:
					if self.x[dimension] == 1:
						evolution.x[dimension] = 0
					elif self.x[dimension] == 0:
						evolution.x[dimension] = 1

		evolution.objective_val = evolution.evaluate_solution(optimization_problem)
		evolution.feasible = evolution.check_feasible(optimization_problem)
		return evolution

	def repair_child_MOKP(self, w, c, lambda_sub, ideal_z):

		m = len(self.objective_val)
		J = [j for j in range(self.n_dim) if self.x[j]==1]
		I = [i for i in range(m) if sum(w[i,j]*self.x[j] for i in range(self.n_dim))>c[i]]
		Qstar = 100000000

		for j in J:
			x_j_minus = self.x
			x_j_minus[j] = 0 # not 1
			Q =  (- utils.g_te(self.x, lambda_sub, ideal_z) + utils.g_te(x_j_minus, lambda_sub, ideal_z))/ sum(w[i,j] for i in I)

			if Qstar > Q:
				Qstar = Q
				kmin = j

		x_j_greedy = self.x
		x_j_greedy[kmin] = 0

		return x_j_greedy


