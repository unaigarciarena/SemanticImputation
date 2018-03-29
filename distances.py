import mutualInfo
import discretization
import toyDB
import interpolation
import numpy as np
import copy
import matplotlib.pyplot as plt
import pandas as pd
import obsSelection as obSel
import imputation
import sequences
from subprocess import check_output
import platform
import argparse
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()

##Used to show the TSs shape (Fig. 4 right now)
def visualize(db, dbInter, dbSimple, dbReg, dbSmooth, dbMax):
    db = np.loadtxt("ts.data", delimiter="\t")
    for i in range(0, dbInter.shape[1]):
        ts = pd.Series(dbInter[:, i])
        ts.plot()
        ts1 = pd.Series(dbSimple[:, i])
        ts1.plot()
        ts2 = pd.Series(dbReg[:, i])
        ts2.plot()
        ts3 = pd.Series(dbSmooth[:, i])
        ts3.plot()
        ts3 = pd.Series(dbMax[:, i])
        ts3.plot()
        ts4 = pd.Series(db[:, i])
        ts4.plot()
        plt.legend(["Interpolation", "Simple", "Regression", "Smooth", "Max", "Original"])

        plt.show()


##Given a Multivariate TS and a list of Multivariate TSs, returns a list with the distances from the first to the others.
##Used for computing distances between original TS to imputed ones
def distances(originalDB, DBlist, d, com):
    table = [0] * len(DBlist)
    for i in range(0, len(DBlist)):
        tot = 0
        importr('TSdist')
        robjects.r('''
                f <- function(d, t1, t2) {
                    t1 = matrix(t1)
                    t2 = matrix(t2)
                    #print(t1[,1])
                    #print(t2)
                    if(d==0){return(STSDistance(t1[,1],t2[,1]))}
                    if(d==1){return(ARLPCCepsDistance(t1[,1],t2[,1]))}
                    if(d==2){return(IntPerDistance(t1[,1],t2[,1]))}
                    if(d==3){return(TquestDistance(t1[,1],t2[,1],2.5))}
                    if(d==4){return(DTWDistance(t1[,1],t2[,1]))}
                    if(d==5){return(ERPDistance(t1[,1],t2[,1],0))}
                    return(-1)
                    }
                ''')
        r_f = robjects.r['f']

        res = r_f(d, originalDB[:, 4], DBlist[i][:, 4])
        table[i] = np.array(res)[0]
    return (table)


##This is the main function
##This function computes all the possible IMs for three DBs in TSDist R package and the sinthetic one.
##Also computes distance between original and imputed ones, and writes down the distances.
def distanceTable(d, size, run):
    if platform.system() == "Linux":
        com = "Rscript"
    elif platform.system() == "Windows":  ##In Windows, Rscript.exe
        com = "Rscript.exe"

    db, fulldb = toyDB.toyGenerator("toydb.csv", size)  ##db contains the MTS with MD, fulldb is the complete original

    ##The working strategy is:
    ## 1 The DB with lost values is cloned in a different object.
    ## 2 That same clone collects the imputed value.
    ## 3 Distances between the original and imputed TSs are computed and saved.

    Ddb = copy.copy(db)
    Ddb = discretization.discretize(Ddb)  ##Ddb contains 0-3 discretized db

    mim = mutualInfo.MIMatrix(Ddb)  ##mim consains (upper diag.) matrix representing mutual info between TSs

    dblInter = copy.copy(db)
    dblInter = interpolation.linearInterpolation(dblInter)  ##Linear interpolation imputation

    dbpInter = copy.copy(db)
    dbpInter = interpolation.pchipInterpolation(dbpInter)  ##Pchip interpolation imputation

    dbqInter = copy.copy(db)
    dbqInter = interpolation.quadInterpolation(dbqInter)  ##Quadratic interpolation imputation

    dbsInter = copy.copy(db)
    dbsInter = interpolation.splineInterpolation(dbsInter)  ##Spline interpolation imputation

    dbKalman = copy.copy(db)
    dbKalman = imputation.tsImputation(dbKalman, com)  ##Seasonally splitted Kalman based Imputation

    dbSimple = copy.copy(db)
    dbSimple = imputation.simple(dbSimple, com, 0)  ##EM imputation

    db1Simple = copy.copy(db)
    db1Simple = imputation.simple(db1Simple, com, 1)  ##MICE imputation

    dbFullReg = copy.copy(dbSimple)
    dbFullReg = imputation.regression(db, dbFullReg, Ddb, mim, 1)  ##Full regression (esto es una combinacion de métodos)

    dbRegKal = copy.copy(dbKalman)
    dbRegKal = imputation.regression(db, dbRegKal, Ddb, mim, 0)  ##Polished Kallman regression
    aux = distances(fulldb,
                    [dblInter, dbpInter, dbqInter, dbsInter, dbKalman, dbSimple, db1Simple, dbFullReg, dbRegKal], d,
                    com)

    print(d, aux)
    np.savetxt("outputs/Len" + str(size) + "D" + str(d) + "R" + str(run) + ".csv", aux)

    return (aux)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'integers', metavar='int', type=int, choices=range(10),
        nargs=1, help='number of generated instances for each DB/MDtype')

    args = parser.parse_args()
    #missing_lengths = [1,3,5,8,10,11,12,13,14,15,16,17,20,25,30,35,50]
    missing_lengths = [1,5,10,15,20,25,30]
    runs = range(30)
    ds = [4]
    for run in runs:
        for d in ds:
            for length in missing_lengths:
                distanceTable(d, length, run)