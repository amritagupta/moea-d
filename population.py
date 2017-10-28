# Definition of the population class


import solution.py
import SubProblem.py
import lam_nbd.py

class Population(object):

    """
    A population is a set of solutions. It has te following arguments:
    list_of_solution : list of solutions of the population
    ideal_Z : Ideal point of the solutions
    """

    def _init_(self, number_of_solution, list_of_subporblems):

        """
        :param number_of_solution: The size of the population, how many solutions it will contain
        :param list_of_solutions: the list of solution of the population
        :param ideal_Z: the ideal point of the population (in objective space)
        :return: create a new instance population
        """

        self.number_of_solution = number_of_solution

        for subproblem in list_of_subporblems:
            sol = SubProblem.cur_solution
            self.list_of_solutions.append(sol)

        self.ideal_Z = self.compute_ideal_z(self.list_of_solution)



    def compute_ideal_z(list_of_solution):

        """
        Compute the values of the coordinates of the ideal point for the list of solution received
        :param list_of_solution: A list of solution, which include decision space coordinates and objective values
        :return: One solution which is the ideal point of the list of solution
        """

        ideal_Z  = [None] * len(list_of_solution[0].objective_val)

        for solution in list_of_solution:
            for value in solution.objective_val:
                if ideal_Z[value] == None:
                    ideal_Z[value] = value
                if value < ideal_Z:
                    ideal_Z[value] = value

        return ideal_Z

    Solution(30, ['Con'])

