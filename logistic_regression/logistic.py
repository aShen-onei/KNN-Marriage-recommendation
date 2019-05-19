import numpy as np
import math
import matplotlib.pyplot as plt

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
    return  1.0 / (1+np.exp(-inX))
    # return 1.0/(1+np.exp(-2*inX))-1
# 正常梯度算法
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
        error = lableMat - h
        # 矩阵乘法？迭代得出回归系数？
        weights = weights + alpha * dataMatrix.transpose() * error
    return np.array(weights)
# 梯度下降算法
def stocGradAscent1(dataMatrix, classLables):
    m, n = np.shape(dataMatrix)
    alpha = 0.01
    weights = np.ones(n)
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i] * weights))
        error = classLables[i] - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights

# 可视化展示
def plotFit(dataArr, lableMat, weights):
    dataArr = np.array(dataArr)
    n = np.shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(lableMat[i]) == 1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=20, c='red', marker='s', alpha=.5)  # 绘制正样本
    ax.scatter(xcord2, ycord2, s=20, c='green', alpha=.5)  # 绘制负样本
    x = np.arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x, y)
    plt.title('BestFit')  # 绘制title
    plt.xlabel('X1'); plt.ylabel('X2')  # 绘制label
    plt.show()


if __name__ == '__main__':
    dataMat, lableMat = loadfile('testSet.txt')
    weights = gradAscent(dataMat, lableMat)
    plotFit(dataMat, lableMat, weights)