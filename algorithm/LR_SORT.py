import KNN as kNN
import numpy as np
import sys
import pymysql
import re
import requests
import json
import random

def sigmoid(inX):
    return 1.0/(1+np.exp(-inX))

def randomAscent(dataMatrix, classLable, numIter=150):
    m, n = np.shape(dataMatrix)
    weights = np.ones(n)
    for j in range(numIter):
        dataIndex = list(range(m))
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.01
            randIndex = int(random.uniform(0, len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLable[randIndex]-h
            weights = weights+alpha*error*dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def classfy(inX, weights):
    pro = sigmoid(sum(inX*weights))
    print(pro)

def colictest():
    frTrain = open('../train/logisticTrain.txt')
    trainingSet = []
    trainingLable = []
    for line in frTrain.readlines():
        currline = line.strip().split('\t')
        lineArr = []
        for i in range(len(currline)-1):
            lineArr.append(float(currline[i]))
        trainingSet.append(lineArr)
        trainingLable.append(float(currline[-1]))
    trainweights = randomAscent(np.array(trainingSet), trainingLable, 500)
    return trainweights
def test(weights):
    fr = open('../train/logisticTrain.txt')
    for line in fr.readlines():
        currline2 = line.strip().split('\t')
        lineArr2 = []
        for i in range(len(currline2) - 1):
            lineArr2.append(float(currline2[i]))
        classfy(np.array(lineArr2), weights)

if __name__ == "__main__":
    weights = colictest()
    test(weights)