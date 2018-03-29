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
        for j in range(0, originalDB.shape[1]):
            aux = check_output(com + ' TSdist' + str(d) + '.r ' + " ".join(
                map(str, np.round(originalDB[:, j], decimals=4))) + " 0 " + " ".join(
                map(str, np.round(DBlist[i][:, j], decimals=4))), shell=True)
            if aux[4] == "N":
                print("NA")
                aux = 0.0
            else:
                aux = np.float(aux[4:])
            table[i] = table[i] + aux
        table[i] = table[i] / originalDB.shape[1]
    return (table)


##This is the main function
##This function computes all the possible IMs for three DBs in TSDist R package and the sinthetic one.
##Also computes distance between original and imputed ones, and writes down the distances.
def distanceTable(d, size):
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
    dbFullReg = imputation.regression(db, dbFullReg, Ddb, mim, 1)  ##Full regression

    dbRegKal = copy.copy(dbKalman)
    dbRegKal = imputation.regression(db, dbRegKal, Ddb, mim, 0)  ##Polished Kallman regression
    aux = distances(fulldb,
                    [dblInter, dbpInter, dbqInter, dbsInter, dbKalman, dbSimple, db1Simple, dbFullReg, dbRegKal], d,
                    com)

    print(d, aux)
    np.savetxt("outputs/Len" + "D" + str(d) + ".csv", aux)

    return (aux)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'integers', metavar='int', type=int, choices=range(10),
        nargs=1, help='number of generated instances for each DB/MDtype')

    args = parser.parse_args()
    d = args.integers[0]  ##distance
    missing_lengths = [1,3,5,8,10,11,12,13,14,15,16,17,20,25,30,35,50]
    for length in missing_lengths:
        distanceTable(d, length)