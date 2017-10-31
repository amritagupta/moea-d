#!/opt/python/bin/python

import numpy as np

def obj_eval(F,x):
    m = len(F) # number of rows
    for i in range(m):
        FV[i]=np.dot(F[i],x)
    return FV
    
    