#!/opt/python/bin/python

import numpy as np

def g_te(xA,lambda_sub, ideal_z):
    gte = np.max(np.multiply(lambda_sub, np.abs(np.subtract(xA.objective_val, ideal_z) ) ) )
    
    return gte