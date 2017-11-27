#!/usr/bin/python
"""
This module defines objects related to the population in the MOEA/D genetic algorithm.
"""
import numpy as np
import random
import utils as utils

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
	def __init__(self, n_dim, num_type, subproblem):
		"""
		Construct a new 'Solution' instance by random generation.
		:param n_dim: The number of dimensions the solution has.
		:param num_type: The numeric type of each dimension.
		:param subproblem: The subproblem number to which it is a solution.
		"""
		super(Solution, self).__init__()
		self.n_dim = n_dim
		self.generation = 1
		self.subproblem = subproblem
		self.feasible = False
		self.objective_val = None
		self.x = [None]*n_dim
		self.num_type = num_type

		if not len(num_type) == n_dim:
			raise ValueError('The number of dimensions does not match the length of the numeric type specification.')
		for i in range(n_dim):
			if num_type[i] == 'Binary':
				# generate 0 or 1
				self.x[i] = np.random.randint(2)
			elif num_type[i] == 'Continuous':
				# generate random real number between 0 and 1
				self.x[i] = np.random.uniform()

		self.objective_val = self.evaluate_solution('ZDT1')
		self.feasible = self.check_feasible('ZDT1')

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

	def check_feasible(self, optimization_problem):
		"""
		Check that a solution x satisfies constraints in the optimization_problem.
		:param optimization_problem: For now, only evaluates ZDT1
		"""
		if optimization_problem == 'ZDT1':
			n = len(self.x)
			if not n == 30:
				raise ValueError('The solution needs to have dim 30 for the ZDT1 test instance.')
		any_constraint_violated = False
		solution_feasible = True
		for i in range(n):
			if self.x[i] > 1 or self.x[i] < 0:
				any_constraint_violated = True
				break
		if any_constraint_violated:
			solution_feasible = False
		else:
			solution_feasible = True

		return solution_feasible

	def crossover_operator(self, solution2, generation):
		"""
		Do cross over operations on 2 parents, choosing the best child with the g function
		"""
		crossover_point = random.choice(range(1, self.n_dim - 1))

		new_solution1 = Solution(self.n_dim, self.num_type, self.subproblem)
		new_solution2 = Solution(self.n_dim, self.num_type, self.subproblem)
		new_solution1.generation = generation
		new_solution2.generation = generation

		for dimension in range(0, self.n_dim - 1):
			if dimension < crossover_point:
				new_solution1.x[dimension] = self.x[dimension]
				new_solution2.x[dimension] = solution2.x[dimension]
			elif dimension >= crossover_point:
				new_solution1.x[dimension] = solution2.x[dimension]
				new_solution2.x[dimension] = self.x[dimension]

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

		if self.num_type[mutated_dimension] == 'Continuous':
			evolution.x[mutated_dimension] = self.x[mutated_dimension] + np.random.normal(0, self.x[mutated_dimension]^2 + 1)

		elif self.num_type[mutated_dimension] == 'Binary':
			if self.x[mutated_dimension] == 1:
				evolution.x[mutated_dimension] = 0
			elif self.x[mutated_dimension] == 0:
				evolution.x[mutated_dimension] = 1

		return evolution

	def mutation_operator2(self, frequency_of_change):
		"""
		Do mutation operation on a solution
		"""
		evolution = self

		for dimension in range(0, self.n_dim - 1):

			if self.num_type[dimension] == 'Continuous':
				change = np.random.binomial(1, frequency_of_change)
				if change == 1:
					#print(self.x[dimension])
					evolution.x[dimension] = self.x[dimension] + np.random.normal(0, self.x[dimension]**2 + 1)

			elif self.num_type[dimension] == 'Binary':
				change = np.random.binomial(1, frequency_of_change)
				if change == 1:
					if self.x[dimension] == 1:
						evolution.x[dimension] = 0
					elif self.x[dimension] == 0:
						evolution.x[dimension] = 1

		return evolution
 def repair_child(self, w, c):
   m = len(self.objective_val)
   J = [j if self.x[j]==1 for j in range(self.n_dim)]
   I = [i if sum(w[i,j]*self.x[j] for i in range(n_dim))>c[i] for i in range(m)]
