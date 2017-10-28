#!/opt/python/bin/python

from __future__ import print_function
import sys
print(sys.argv)

import numpy as np

def obj_eval(F,x):
    #n = len(x)
    m = len(F) # number of rows
    for i in range(m):
        FV[i]=np.dot(F[i],x)
    return FV
    
    