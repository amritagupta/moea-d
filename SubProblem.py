#!/opt/python/bin/python

class SubProblem(object):
    "" 
    A single instance of a SubProblem has the following properties:
        Attributes:
            index: index of the subproblem
            lambda: the weight vector of the current subproblem (scalarization weights)
            B: neighborhood of T indices of nearest lambdas
            cur_solution: current solution to the subproblem (n by 1)
            #FV: vector of objective values evaluated at cur_solution (m by 1)
    ""
    def _init_(self, index, lambda, B, cur_solution):
        ""
        Construct a new SubProblem instance by initialization. 
        :param lambda: the weight vector of the current subproblem (scalarization weights)
        : param B:  neighborhood of T indices of nearest lambdas
        ""
        super(SubProblem,self)._init_()
        self.index = index
        self. lambda = lambda
        self.B = B
        self.cur_solution = cur_solution
        