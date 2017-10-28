#!/usr/bin/python
"""
This module defines objects related to the population in the MOEA/D genetic algorithm.
"""
import numpy as np

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


### Test Area
sol = Solution(30, ['Continuous']*30, 2)

