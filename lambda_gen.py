#!/opt/python/bin/python

from __future__ import print_function
import sys
print(sys.argv)
import os
import csv
import time
import random
import numpy as np
from scipy.special import comb

def lambda_gen(m,n):
    H = 25
    N = comb(H+m-1, m-1)
    for i in range(N): 
        for k in range(m):
            lam[i, k] = float(1/H)*random.choice(range(H+1))
            # each roq is one lambda vector with m weights
        lam[i,:]=float(1/sum(lam[i,:]))*lam[i,:]
    return lam