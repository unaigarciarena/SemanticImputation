import numpy as np
import math
   
##The limits that will determine the discrete number of a continuous value
##Now it splits the vector in three equal parts    
def setLimits(ts):
    ##Delete NaNs
    ts = [value for value in ts if not math.isnan(value)]
    ##Sort valid values
    x = np.sort(ts)
    ##Determine discretization limits bay obtaining the top values in the first and second thirds.
    return(x[x.shape[0]//3], x[x.shape[0]*2//3])

##Principal function
def discretize(db):

    for i in range(0, db.shape[1]):
        low, up = setLimits(db[:,i])
        ##If NaN = 0
        ##If smaller than low limit (thus smaller than upper limit), 1
        ##If greater than low and smaller than upper, 2
        ##If greater than both low and upper, 3
        db[:,i] = [int(1 + int(value>low) + int(value>up)) if np.isfinite(value) else 0 for value in db[:,i]]
    return db