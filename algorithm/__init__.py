import KNN as kNN
import numpy as np
import sys
sys.path.append('../traindata/')
import manreplite as getlocal
"""
filename = '../testdata/dataSet.txt'
"""
if __name__ == "__main__":
    dataSet, lable = kNN.dataSetAnalyse('../testdata/dataSet.txt')
    stdDataSet, averageVals, ranges = kNN.standardization(dataSet)
    lng, lat = getlocal.getLocation_json('大连')
    nyarry = np.array([1, 175.0, 3.0, 7500.0, lng, lat, 27])
    testArray = nyarry - averageVals/ranges
    kNN.kNN(testArray, stdDataSet, lable, 10)