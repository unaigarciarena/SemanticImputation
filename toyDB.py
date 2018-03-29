import math
import numpy as np
from subprocess import check_output
import os
import copy
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib
import platform
import pandas as pd

##Visualize the Sinthetic DB
def visualize(db, x):

    labels = ["y = x", "y = 2x", "y = sin(x)", "y = cos(x)", "y = ln(x)"]
    plt.title("DB " + str(x) + " representation")    
    markers = []
    for m in Line2D.markers:
        try:
            if len(m) == 1 and m != ' ':
                markers.append(m)
        except TypeError:
            pass

    for i in range(0, db.shape[1]):
        if x == 0:
            plt.plot(db[:,i], label = labels[i], marker = markers[i])
        else:
            plt.plot(db[:,i])
    
    matplotlib.rcParams.update({'font.size': 28})
    plt.xlabel("t", size = "xx-large")
    plt.ylabel("f(t)     ", size = "xx-large", rotation = 0)
    plt.legend(loc = 'upper left', prop = {"size":24})
    plt.show()
    
##Visualization of the MD introduction (Fig. 5 right now)
def visualizeMD(ts, tscom):
    markers = []
    for m in Line2D.markers:
        try:
            if len(m) == 1 and m != ' ':
                markers.append(m)
        except TypeError:
            pass
    plt.title("MD introduction example")
    plt.plot(tscom, label = "Missing chunks", color = "c", marker = markers[3], markersize = 10)
    plt.plot(ts, label = "Complete TS", color = "k", marker = markers[1], markersize = 10)
    plt.legend(loc = 'upper left', prop = {"size":24})
    matplotlib.rcParams.update({'font.size': 28})
    plt.xlabel("t", size = "xx-large")
    plt.ylabel("f(t)     ", size = "xx-large", rotation = 0)
    plt.show()

##Generates Sinthetic DB (If i == 0) or imports the ones in TSdist (if 0<i<4)
def toyGenerator(path, size):
    ## Artificial DB for i = 0
    db = pd.read_csv("Dataset.csv", delimiter=";", date_parser=["date"], infer_datetime_format=True)
    db["date"] = pd.to_numeric(pd.to_datetime(db["date"]))
    db["date"] = db["date"] - np.min(db["date"])
    db["date"] = db["date"] / np.max(db["date"])
    db = db.as_matrix()
    compDb = copy.copy(db)
	
	
    ##Introduce punctual NaNs
    for i in range(0,int(db.shape[0]*0.3/size)):
        ##Introduce 132 NaN randomly
        aux = np.random.randint(0, db.shape[0]-size)
        db[aux:aux+size, 4] = np.nan
        ##Modify 20 values
        #db[np.random.randint(0, db.shape[0]),np.random.randint(0, db.shape[1])] *= 1.5"""

    """for i in range(3,10):
        ##Insert NaN sequences
        aux = np.random.randint(0, db.shape[0]-i-10)
        db[range(aux, aux+i+10), np.random.randint(0, db.shape[1])] = np.nan#"""
    
    np.savetxt(path, db, delimiter = "\t", fmt='%1.3f')
    return(db, compDb)
    
"""i = 1
a,b = toyGenerator("hueuhe.data", i)
for i in range(0, a.shape[1]):
    visualizeMD(a[:,i], b[:,i])
"""
#visualize(b, i)