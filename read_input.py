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

def read_input():
    rd = []
    with open('zdt1.lp', 'rb') as ex:
        rd = list(csv.reader(ex, skipinitialspace=True))
        rd = [i for i in rd if i]