import numpy as np
import math
import sklearn.metrics

def MIMatrix(db):
    mim = np.zeros((db.shape[1],db.shape[1]))
    ##For every TS combination possible
    for i in range(0, db.shape[1]):
        for j in range(i+1, db.shape[1]):
            ##Compute Mutual information.
            mim[i,j] = sklearn.metrics.normalized_mutual_info_score(db[:,i], db[:,j])
    return mim
