import KNN as kNN
import numpy as np
import sys
import pymysql
import re
import requests
import json
import random
from sklearn.linear_model import LogisticRegression

def sigmoid(inX):
    return 1.0 / (1 + np.exp(-inX))

def randomAscent(dataMatrix, classLable, numIter):
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
    return pro

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
    trainweights = randomAscent(np.array(trainingSet), trainingLable, 3500)
    return trainweights
def test(weights):
    fr = open('../testdata/logisticTest.txt')
    res = []
    for line in fr.readlines():
        currline2 = line.strip().split('\t')
        lineArr2 = []
        for i in range(len(currline2) - 1):
            lineArr2.append(float(currline2[i]))
        res.append(classfy(np.array(lineArr2), weights))
    res = np.array(res)
    sort_proIndex = res.argsort()
    print(len(sort_proIndex))
    index_array = []
    for i in range(len(sort_proIndex)):
        if res[sort_proIndex[i]] < 0.5:
            continue
        else:
            index_array.append(sort_proIndex[i])
    print(len(index_array))
    return index_array
'''
利用skLearn算法工具中的逻辑回归预测
但是不能计算出值。。。。。很残念
# 逻辑回归预测
def colicSklearn():
    frTrain = open('../train/logisticTrain.txt')
    trainingSet = []
    trainingLable = []
    for line in frTrain.readlines():
        currline = line.strip().split('\t')
        lineArr = []
        for i in range(len(currline) - 1):
            lineArr.append(float(currline[i]))
        trainingSet.append(lineArr)
        trainingLable.append(float(currline[-1]))
    classifier = LogisticRegression(solver='sag', max_iter=500).fit(trainingSet, trainingLable)
    pro = classifier.predict_log_proba(trainingSet)
    pro2 = classifier.get_params()
    print(pro)
    print(pro2)
'''
def main():
    weights = colictest()
    index = test(weights)
    return index