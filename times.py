import toyDB
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import copy
import imputation
import discretization
import mutualInfo
import platform
import argparse


##Time recording function
def times(id):

	times = np.zeros((6, 6))

	if platform.system() == "Linux":
		com = "Rscript"  
	elif platform.system() == "Windows": ##In Windows, Rscript.exe
		com = "Rscript.exe"

	for j in range(0,6):

		db, fulldb = toyDB.toyGenerator("toydb.csv", 2)

		for k in range(0, j):
			db = np.concatenate((db,db))
			fulldb = np.concatenate((fulldb,fulldb))

		aux = dt.datetime.now()

		Ddb = copy.copy(db)
		Ddb = discretization.discretize(Ddb)
					
		mim = mutualInfo.MIMatrix(Ddb)

		times[j, 0] = (dt.datetime.now()-aux).total_seconds()
		aux = dt.datetime.now()

		dbSimple = copy.copy(db)
		dbSimple = imputation.simple(dbSimple, com, 0)
		

		times[j, 1] = (dt.datetime.now()-aux).total_seconds()
		
		aux = dt.datetime.now()

		dbSimple1 = copy.copy(db)
		dbSimple1 = imputation.simple(dbSimple1, com, 1)
		

		times[j, 2] = (dt.datetime.now()-aux).total_seconds()
		
		aux = dt.datetime.now()

		dbFullReg = copy.copy(dbSimple)
		dbFullReg = imputation.regression(db, dbFullReg, Ddb, mim, 1)

		times[j, 3] = (dt.datetime.now()-aux).total_seconds()
		aux = dt.datetime.now()

		dbReg = copy.copy(dbSimple)
		dbReg = imputation.regression(db, dbReg, Ddb, mim, 0)
			  
		times[j, 4] = (dt.datetime.now()-aux).total_seconds()
		aux = dt.datetime.now()

		dbKalman = copy.copy(db)
		dbKalman = imputation.tsImputation(dbKalman, com)

		times[j, 5] = (dt.datetime.now()-aux).total_seconds()
			
	np.savetxt("times" + str(id) + ".csv", times)
	
if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument(
		'integers', metavar='int', type=int, 
		 nargs=1, help='jobid')
		 
	args = parser.parse_args()
	id = args.integers[0]
	
	times(id)