from sklearn.linear_model import logistic
import numpy as np
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

def colictest():
    frTrain = open('horseColicTraining.txt')
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
    print(trainweights)
    errorCount = 0
    numTestVec = 0.0
    for line in frTrain.readlines():
        numTestVec += 1.0
        currline = line.strip().split('\t')
        lineArr = []
        for i in range(len(currline)-1):
            lineArr.append(float(currline[i]))
        if int(classfy(np.array(lineArr), trainweights)) != int(currline[-1]):
            errorCount+=1
    errorRate = (float(errorCount)/numTestVec) * 100
    print(errorRate)

def classfy(inX, weights):
    pro = sigmoid(sum(inX*weights))
    if pro>0.5:
        return 1.0
    else:
        return 0.0

if __name__ == '__main__':
    colictest()
