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


#PARAMETERS_______________________

T = 10 # number of neighbors