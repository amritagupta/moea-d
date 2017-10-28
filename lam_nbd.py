#!/opt/python/bin/python

from __future__ import print_function
import sys
print(sys.argv)
import random
import numpy as np
from sklearn.neighbors import NearestNeighbors

def lam_nbd(lam, T=10):
    N = len(lam)  # number of rows of lam
    B = np.empty([N,T+1],int)
    nbrs = NearestNeighbors(n_neighbors=T+1, algorithm='ball_tree', metric='euclidean').fit(lam)
    distances, B = nbrs.kneighbors(lam)
    for i in range(N):
        B[i,:] = B[i,1:T+1]