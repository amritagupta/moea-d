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
    
list_of_solution = [subprob.cur_solution for subprob in subproblem_list]
ideal_Z  = [None] * m
for solution in list_of_solution:
    for value in solution.objective_val:
        if ideal_Z[value] == None:
            ideal_Z[value] = value
        if value < ideal_Z:   #minimizing 
            ideal_Z[value] = value

EP = []
MAXGEN = 5
for generation in range(MAXGEN):
    for i in range(N): # for each subproblem
        parents = np.random.choice(subproblem_list[i].B,2,replace = False)
        offspring = genetic(parents)         #Genetic Operators
        offspring = repair(offspring)
        for k in range(m):
            population.ideal_Z = np.minimum(population.ideal_Z,offspring)   # minimizing
        for j in subproblem_list[i].B:
            if g_te(offspring,subproblem_list[j].lambda, population.ideal_Z) <= g_te(subproblem_list[j].cur_solution,subproblem_list[j].lambda, population.ideal_Z):
                subproblem_list[j].cur_solution = offspring
        EP = pop_dom_check_update(EP, offspring)
        

            
            
            
            
            
            
       
        
        