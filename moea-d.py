#!/opt/python/bin/python

from __future__ import print_function
import sys
print(sys.argv)
import os
import csv
import time
import random
import numpy as np
from numpy.random import choice
from gurobipy import*
from sklearn.neighbors import NearestNeighbors

from lambda_gen import lambda_gen
from lam_nbd import lam_nbd
from SubProblem import SubProblem
from solution import solution
#PARAMETERS_______________________

T = 10 # number of neighbors
n = 30
m = 2
lam = lambda_gen(m,n)
B = lam_nbd(lam)
N = len(lam)
subproblem_list = []
for i in range(N):
    temp_sol = solution(n,['Continuous']*n,i)
    while not temp_sol.feasible:
        temp_sol = solution(n, ['Continuous'] * n, i)
    temp_sub = SubProblem(i,lam[i,:],B[i,:],temp_sol)
    subproblem_list.append(temp_sub)
    
    #index, lambda, B, cur_solution)