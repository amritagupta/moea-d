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
#PARAMETERS_______________________

T = 10 # number of neighbors
lam = lambda_gen(3, 30,25)