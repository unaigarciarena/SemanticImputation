import pandas as pd
import numpy as np
import sequences as sq
import copy
import toyDB
import imputation
import discretization
import mutualInfo
import matplotlib.pyplot as plt
            
##This function determines the sequence that will be used to interpolate
##Not used right now
def pointSelector(seq):
   ##Sequences will have two times as much points to interpolate as their length.
    for i in range(0, len(seq)):
        x = seq[i]
        if len(x) == 2: ##If there are not known points inside the lost sequence, compute length
            length = max(x[1]-x[0],4)
        else: ##If there are known points inside the missing sequence, compute the amount of missing values
            length = max(x[1]-x[0]-x[2],4)
        ##In the best case, each sequence will have four times its length to interpolate values
        seq[i] = (max(x[0]-length*2,0), x[1]+(length)*2)
            
    return seq 
    
##Multiple principal function
##Not used right now
def multInterpolation(db):

    for i in range(0, db.shape[1]):
        ts = db[:,i]
        seq = sq.detectSequences(ts) 
        if len(seq)>1: ##In case there are more than one sequence
            seq = sq.joinSequences(seq) ##Join sequences in case they are relatively close
        seq = pointSelector(seq) ##Select points
        for j in range(0, len(seq)):
            s = pd.Series(ts[seq[j][0]:seq[j][1]])
            ##Three types are considered, combining to a simple Multiple Imputation Algorithm.
            s1 = s.interpolate(method = "polynomial", order = int(min(s.notnull().sum()-1, 4)))
            s2 = s.interpolate(method = "spline", order = int(min(s.notnull().sum()-1, 3)))
            s3 = s.interpolate(method = "cubic")
            db[seq[j][0]:seq[j][1],i] = (s1.values + s2.values + s3.values)/3
    ##In case values are lost at the beggining or the end of the TS,        
    db = (pd.DataFrame(db)).fillna(method='pad').as_matrix()
    db = (pd.DataFrame(db)).fillna(method='bfill').as_matrix()
    return(db)

## Given a Full DB (in this case, filled by regression) and the empty DB, returns an inttermitently smoothed imputed DB.
## Not used right now
def performSmoothing(db, complDb, seq):
    complDb1 = copy.copy(complDb) ##Two copies of the same DB
    ##For each ts in Multivariate TSs
    for i in range(0, db.shape[1]):
        ts = db[:,i]
        ## For each long sequence
        for j in range(0, len(seq[i])):
            #print(seq[j])
            #print(seq[j][0], seq[j][1])
            l = seq[i][j][1]-seq[i][j][0] ##Compute sequence length
            if l > 2:
                l1 = np.int(np.log(l))*2 ## The sequence is divided in chunks of length ln(total length)
                k = 0
                while k*l1 < l:
                    ##Each copy will have complementary NaN of each sequence
                    complDb1[seq[i][j][0]+k*l1:min(seq[i][j][0]+(k+1)*l1, seq[i][j][1]), i] = np.nan
                    complDb[seq[i][j][0]+(k+1)*l1:min(seq[i][j][0]+(k+2)*l1, seq[i][j][1]), i] = np.nan
                    k = k+2
    ##Perform interpolation of both complementary DBs
    complDb = performInterpolation(complDb)
    complDb1 = performInterpolation(complDb1)

    return((complDb + complDb1)/2)
	
##Linear principal function
def linearInterpolation(db):

    for i in range(0, db.shape[1]):
        ts = db[:,i]
        seq = sq.detectSequences(ts) 
        if len(seq)>1: ##In case there are more than one sequence
            seq = sq.joinSequences(seq) ##Join sequences in case they are relatively close
        seq = pointSelector(seq) ##Select points
        for j in range(0, len(seq)):
            s = pd.Series(ts[seq[j][0]:seq[j][1]])
            db[seq[j][0]:seq[j][1],i] = (s.interpolate(method = "linear")).values
    ##In case values are lost at the beggining or the end of the TS,        
    db = (pd.DataFrame(db)).fillna(method='pad').as_matrix()
    db = (pd.DataFrame(db)).fillna(method='bfill').as_matrix()
    return(db) 
	
##Quadratic principal function
def quadInterpolation(db):
    #a = db[:,4]
    for i in range(0, db.shape[1]):
        ts = db[:,i]
        seq = sq.detectSequences(ts) 
        if len(seq)>1: ##In case there are more than one sequence
            seq = sq.joinSequences(seq) ##Join sequences in case they are relatively close
        seq = pointSelector(seq) ##Select points
        for j in range(0, len(seq)):
            s = pd.Series(ts[seq[j][0]:seq[j][1]])
            db[seq[j][0]:seq[j][1],i] = (s.interpolate(method = "quadratic")).values
    ##In case values are lost at the beggining or the end of the TS,        
    db = (pd.DataFrame(db)).fillna(method='pad').as_matrix()
    db = (pd.DataFrame(db)).fillna(method='bfill').as_matrix()

    return(db)    
	
##Spline principal function
def splineInterpolation(db):

    for i in range(0, db.shape[1]):
        ts = db[:,i]
        seq = sq.detectSequences(ts) 
        if len(seq)>1: ##In case there are more than one sequence
            seq = sq.joinSequences(seq) ##Join sequences in case they are relatively close
        seq = pointSelector(seq) ##Select points
        for j in range(0, len(seq)):
            s = pd.Series(ts[seq[j][0]:seq[j][1]])
            db[seq[j][0]:seq[j][1],i] = (s.interpolate(method = "spline", order = 2)).values
    ##In case values are lost at the beggining or the end of the TS,        
    db = (pd.DataFrame(db)).fillna(method='pad').as_matrix()
    db = (pd.DataFrame(db)).fillna(method='bfill').as_matrix()
    return(db)
	
##krogh principal function
##Not used right now
def kroghInterpolation(db):

    for i in range(0, db.shape[1]):
        ts = db[:,i]
        seq = sq.detectSequences(ts) 
        if len(seq)>1: ##In case there are more than one sequence
            seq = sq.joinSequences(seq) ##Join sequences in case they are relatively close
        seq = pointSelector(seq) ##Select points
        for j in range(0, len(seq)):
            s = pd.Series(ts[seq[j][0]:seq[j][1]])
            db[seq[j][0]:seq[j][1],i] = (s.interpolate(method = "krogh")).values
    ##In case values are lost at the beggining or the end of the TS,        
    db = (pd.DataFrame(db)).fillna(method='pad').as_matrix()
    db = (pd.DataFrame(db)).fillna(method='bfill').as_matrix()
    return(db)
	
##pchip principal function
def pchipInterpolation(db):

    for i in range(0, db.shape[1]):
        ts = db[:,i]
        seq = sq.detectSequences(ts) 
        if len(seq)>1: ##In case there are more than one sequence
            seq = sq.joinSequences(seq) ##Join sequences in case they are relatively close
        seq = pointSelector(seq) ##Select points
        for j in range(0, len(seq)):
            s = pd.Series(ts[seq[j][0]:seq[j][1]])
            db[seq[j][0]:seq[j][1],i] = (s.interpolate(method = "pchip")).values
    ##In case values are lost at the beggining or the end of the TS,        
    db = (pd.DataFrame(db)).fillna(method='pad').as_matrix()
    db = (pd.DataFrame(db)).fillna(method='bfill').as_matrix()
    return(db)
	
##Akima principal function
##Not used right now
def akimaInterpolation(db):

    for i in range(0, db.shape[1]):
        ts = db[:,i]
        seq = sq.detectSequences(ts) 
        if len(seq)>1: ##In case there are more than one sequence
            seq = sq.joinSequences(seq) ##Join sequences in case they are relatively close
        seq = pointSelector(seq) ##Select points
        for j in range(0, len(seq)):
            s = pd.Series(ts[seq[j][0]:seq[j][1]])
            db[seq[j][0]:seq[j][1],i] = (s.interpolate(method = "akima")).values
    ##In case values are lost at the beggining or the end of the TS,        
    db = (pd.DataFrame(db)).fillna(method='pad').as_matrix()
    db = (pd.DataFrame(db)).fillna(method='bfill').as_matrix()
    return(db)
	
##Derivatives principal function
##Not used right now
def derInterpolation(db):

    for i in range(0, db.shape[1]):
        ts = db[:,i]
        seq = sq.detectSequences(ts) 
        if len(seq)>1: ##In case there are more than one sequence
            seq = sq.joinSequences(seq) ##Join sequences in case they are relatively close
        seq = pointSelector(seq) ##Select points
        for j in range(0, len(seq)):
            s = pd.Series(ts[seq[j][0]:seq[j][1]])
            db[seq[j][0]:seq[j][1],i] = (s.interpolate(method = "from_derivatives")).values
    ##In case values are lost at the beggining or the end of the TS,        
    db = (pd.DataFrame(db)).fillna(method='pad').as_matrix()
    db = (pd.DataFrame(db)).fillna(method='bfill').as_matrix()
    return(db)