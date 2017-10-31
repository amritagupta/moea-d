#!/opt/python/bin/python

import random
import numpy as np
from scipy.misc import comb


def lambda_gen(m, n, H=25):
	N = int(comb(H+m-1, m-1))  # number of subproblems
	lam = np.empty([N,m])
	for i in range(N): 
		for k in range(m):
			lam[i, k] = 1/float(H)*random.choice(range(H+1))
			# each roq is one lambda vector with m weights
		lam[i,:]=float(1/sum(lam[i,:]))*lam[i,:]
	return lam