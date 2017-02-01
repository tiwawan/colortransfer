import numpy as np
import scipy as sp
import numpy.linalg as alg

def HFromPoints(fp, tp):
    A = np.zeros(8,8)
