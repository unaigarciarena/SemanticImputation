import numpy as np
from sklearn.linear_model import Ridge 
import copy
from subprocess import check_output
import matplotlib.pyplot as plt
import pandas as pd
import sequences as sq
import obsSelection as obSel
import os
import random

##Given a complete db, a concrete ts, the observations the regression will be based on and the observations that will
##get its values reimputed, this function performs the regression
def reg(db1, i, obs, miss, full):

	miss = miss.split(" ")
	if miss[len(miss)-1] == "":
		miss = miss[0:len(miss)-2]
	miss = np.array(miss).astype("int")
	if full == 0:
		x = db1[obs]
	elif full ==1:
		x = db1
	y = x[:,i]	
	x = np.delete(x, i, 1)

	impute = db1[miss]
	impute = np.delete(impute, i, 1)
	
	imputer = Ridge()
	imputer.fit(x,y)
	values = imputer.predict(impute)
	db1[miss, i] = values
	return(db1)
	
##Simple IMs
def hd(path, com):
	a = check_output(com + ' hd.r ' + path + " " + os.path.dirname(os.path.abspath(__file__)), shell=True)
	
def mice(path, com):
	a = check_output(com + ' mice.r ' + path + " " + os.path.dirname(os.path.abspath(__file__)), shell=True)
	
def em(path, com):
	a = check_output(com + ' EM.r ' + path + " " + os.path.dirname(os.path.abspath(__file__)), shell=True)
	
def kalman(path, com):
	a = check_output(com + ' kalman.r ' + path + " " + os.path.dirname(os.path.abspath(__file__)), shell=True)

##Perform Kalman Imputation
def tsImputation(db, com):
	np.savetxt("prets.data", db, delimiter = "\t", fmt='%1.3f')
	kalman("prets.data", com)
	db1 = np.genfromtxt("prets1.data", delimiter = "\t", missing_values = "NA")
	data = pd.DataFrame(data = db1).astype(float)
	db1 = data.fillna(method='bfill')
	db1 = data.fillna(method='pad')
	return(db1.as_matrix())
	
##Perform simple imputation
def simple(db, com, im):		
	np.savetxt("pre.data", db, delimiter = "\t", fmt='%1.3f')
	if im == 1:
		mice("pre.data", com)
	elif im == 0:
		em("pre.data", com)
	db1 = np.genfromtxt("pre1.data", delimiter = "\t", missing_values = "NA")
	data = pd.DataFrame(data = db1).astype(float)
	db1 = data.fillna(method='bfill')
	db1 = data.fillna(method='pad')
	return(db1.as_matrix())

##Random Imputation	
def ran(db):
	db1 = copy.copy(db)
	for i in range(0, db.shape[0]):
		for j in range(0, db.shape[1]):
			if np.isnan(db1[i,j]):
				db1[i,j] = random.uniform(np.nanmin(db1[:,j]), np.nanmax(db1[:,j]))
	return(db1)
	
	
##Main regression function. Will perform polished (fullReg == 0) or full (fullReg == 1) regressions. Also, decides
##which	observations need to be selected for polished regression.
def regression(db, dbReg, Ddb, mim, fullReg):
	for i in range(0, dbReg.shape[1]):
		res, cor, values = obSel.bySimilarity(db, mim, i, Ddb)
		for j in range(1, len(res), 2):
			filtered = obSel.obsIndex(Ddb, res[j-1], cor)
			dbReg = reg(dbReg, i, filtered.astype("int"), res[j], fullReg)
	return dbReg

##Combine Regression and Interpolation. Unused in the new experiments
def combineRegInt(seq, dbInt, dbReg):
	for i in range(0, len(seq)):
		for j in range(0, len(seq[i])):
			k = seq[i][j][0]
			l = seq[i][j][1] - seq[i][j][0]
			while k<seq[i][j][1]:
				aux = ((max(np.float(seq[i][j][1]-k)/l, np.float(k-seq[i][j][0])/l)))*0.2
				dbInt[k, i] = dbReg[k, i] * (1-aux) + dbInt[k, i] * aux
				k += 1
	return dbInt