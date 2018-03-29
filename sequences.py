import numpy as np
import pandas as pd

##This function takes a TS and returns the beginning and ending coordinates of all the sequences of MD (even the isolated MVs)
def detectSequences(ts):
    seq = []
    i = 0
    ##For every entry
    while i<ts.shape[0]:
        ## If NaN is found,
        if np.isnan(ts[i]):
            j = i
            ##check the next values
            while j<ts.shape[0] and np.isnan(ts[j]) :
                j += 1
            ##Until a non NaN is found, and save the sequence
            seq += [(i,j)]
            i = j
        i += 1        
    return seq
    
##This function takes a sequence array produced by detectSequences and joins sequences that are relatively near.    
def joinSequences(seq):
    i = 0
    join = []
    ##For every mmissing sequence
    while i < len(seq)-1:
        x = seq[i]
        y = seq[i+1]
        ##If a non missing sequence is smaller than 0.8*len(longest adjacent sequence) the two sequences are set to be joined
        if max(x[1]-x[0], y[1]-y[0])*.8>y[0]-x[1]:
            join += [i-len(join)]
        i += 1
    ##Join the previous selected sequences
    for i in range(0, len(join)):
        x = seq[join[i]]
        y = seq[join[i]+1]
        ##Joined sequences will also contain the number of non missing values between them
        if len(x) == 2:
            seq[join[i]] = (x[0],y[1],y[0]-x[1])
        else:
            seq[join[i]] = (x[0],y[1],y[0]-x[1]+x[2])
        seq.remove(y)
    return seq