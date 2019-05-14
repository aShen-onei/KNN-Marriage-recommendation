import numpy as np
import math

def loadfile(filename):
    dataMat = []
    lableMat = []
    fr = open(filename)
    for line in fr.readlines():
        lineArray = line.strip().split()
        dataMat.append([1.0, float(lineArray[0]), float(lineArray[1])])
        lableMat.append(int(lineArray[2]))
    return dataMat, lableMat

# 训练
def sigmoid(inX):
    # return  1.0 / (1+math.exp(-inX))
    return 1.0 / (1+math.exp(-2*inX)) - 1

def gradAscent(dataMatIn, classLables):
    dataMatrix = np.mat(dataMatIn)
    lableMat = np.mat(classLables).transpose()
    m, n = np.shape(dataMatrix)
    # 步长
    alpha = 0.001
    # 迭代次数
    maxCycles = 500
    weights = np.ones((n, 1))
    for i in range(maxCycles):
        h = sigmoid(dataMatrix*weights)
        error = (lableMat - h)
        # 矩阵乘法？迭代得出回归系数？
        weights = weights + alpha * dataMatrix.transpose() * error

    return np.array(weights)