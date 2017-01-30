import numpy as np
import numpy.linalg as alg

import matplotlib.pyplot as plt

def getHomogMat(sp, dp):
    num_p = sp.shape[0]

    A = np.zeros((2*num_p, 8))

    b = np.zeros((2*num_p, 1))
    
    for i in range(0,num_p):
        A[2*i,:]   = [sp[i,0], sp[i,1], 1, 0,       0,       0, -sp[i,0]*dp[i,0], -sp[i,1]*dp[i,0]]
        b[2*i] = dp[i,0]
        A[2*i+1,:] = [0,       0,       0, sp[i,0], sp[i,1], 1, -sp[i,0]*dp[i,1], -sp[i,1]*dp[i,1]]
        b[2*i+1] = dp[i,1]

    
    h = np.dot(alg.pinv(A), b)



    H = np.matrix([[h[0,0], h[1,0], h[2,0]], [h[3,0], h[4,0], h[5,0]], [h[6,0], h[7,0], 1]])

    print(H)
    return H

def warpWithHomog(points, H):
    num_points = points.shape[0]
    ones = np.ones((num_points,1))
    
    points_hc = np.append(points, ones, axis=1)

    points_warp_hc = points_hc * H.T

    points_warp_hc[:,0] = points_warp_hc[:,0] / points_warp_hc[:,2]
    points_warp_hc[:,1] = points_warp_hc[:,1] / points_warp_hc[:,2]

    return points_warp_hc[:,0:2]

if __name__ == "__main__":
    sp = np.array([[0,0],[1,0],[1,1],[0,1]])
    dp = np.array([[1,1],[2,1],[2,2],[1,2]])
    H = getHomogMat(sp, dp)
    dp_h = warpWithHomog(sp, H)
    print(dp_h)
    
