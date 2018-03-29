import numpy as np
import pandas as pd
import copy
import toyDB
import mutualInfo
import discretization
import imputation
import matplotlib.pyplot as plt

##Given a dependance matrix, returns at least two most related features
def closeFeats(IM):
    cor = []
    while len(cor)<2 or np.any(IM>0.5):
        cFeat = np.argmax(IM)
        IM[cFeat] = 0
        cor = cor + [cFeat  % (IM.shape[0]/2)]

    return cor
    
##This function tags as taboo those features that have too many (20%) coincident missing values with the feature nbeing imputed   
##Unused right now
def filterFeats(Ddb, i):

    j = 0
    taboo = []
    while j<Ddb.shape[1]:
        if not j == i:
            aux = Ddb[:,j] == Ddb[:,i]
            aux1 = Ddb[:,j] == np.zeros(Ddb.shape[0])
            aux = sum(aux & aux1)
            if aux > 0:
                taboo += [j]            
        j += 1
    return(taboo)
    
##Given a matrix in which missing observations in a TS are related to the observations that will most likely perform the best regression,
##this function groups them by the observations. This way, all the MVs that coincide on the regression observations are grouped,
##and regression will only be performed once for all of them    
def groupBy(values):

    res = []
    
    for i in range(0, values.shape[0]):
        aux = ""
        for j in range(1, values.shape[1]):
            aux +=  str(int(values[i,j])) + " "
        if aux in res:
            index = res.index(aux) + 1
            res[index] += " " + str(int(values[i,0]))
        else:
            res = res + [str(aux)] + [str(int(values[i,0]))]
            
    return(res)
    
##Given a db, a dependance matrix, a ts and the discretized db, returns the discretized values of the most related variables
##to select the best observations to perform a regression
def bySimilarity(db, IM, tsIndex, Ddb):
    ts = db[:,tsIndex]
    cor = closeFeats(copy.copy(np.concatenate((IM[:,tsIndex], IM[tsIndex,:]))))
    #cor = np.random.random_integers(0, db.shape[1]-1, size = (2))
    mObs = (np.array(range(0, len(ts))))[np.isnan(ts)]
    values = np.zeros((len(mObs), len(cor)+1))
    values[:,0] = mObs
    for i in range(0, len(mObs)):
        for j in range(0, len(cor)):

            values[i, j+1] = np.mean(Ddb[mObs[i], int(cor[j])])
            
    res = groupBy(values)

    return(res, cor, values)
    
##Given the values of the rest of the DB for a missing observation in the TS being imputed, this functions returns observations in
##the values of the most correlated variables are similar
def obsIndex(Ddb, values, cor):
    values = values.split(" ")
    values = values[0:len(values)-1]
    index = np.zeros((Ddb.shape[0], 1))
    index[:,0] = range(0, Ddb.shape[0])

    Ddb = np.concatenate((Ddb, index), axis = 1)
    filtered = Ddb
    for i in range(0, len(values)):##One or more variables
        filtered = filtered[filtered[:,int(cor[i])] == int(values[i])]
        #filtered = filtered[filtered[:,cor[i]] == np.random.random_integers(1,3)]
    return(filtered[:,filtered.shape[1]-1])    
