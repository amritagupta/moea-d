#!/opt/python/bin/python

class SubProblem(object):
    """
    A single instance of a SubProblem has the following properties:
        Attributes:
            index: index of the subproblem
            lambda: the weight vector of the current subproblem (scalarization weights)
            B: neighborhood of T indices of nearest lambdas
            cur_solution: current solution to the subproblem (n by 1)
            #FV: vector of objective values evaluated at cur_solution (m by 1)
    """
    def __init__(self, index, lam, B, cur_solution):
        """
        Construct a new SubProblem instance by initialization. 
        :param lambda: the weight vector of the current subproblem (scalarization weights)
        : param B:  neighborhood of T indices of nearest lambdas
        """
        super(SubProblem,self).__init__()
        self.index = index
        self.lam = lam
        self.B = B
        self.cur_solution = cur_solution

