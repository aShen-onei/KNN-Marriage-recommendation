import numpy as np
import operator
"""
kNN算法实现：
训练集为testdata文件下的dataSet.txt文件
测试集
K的选取暂定为3
"""

"""
读取训练集，将训练集填入到numpy训练矩阵中
dataSetAnalyse
参数:
     filename:文件夹路径
返回:
     returnMat:数据特征矩阵
     lableVector:标签结果特征向量
"""
def dataSetAnalyse(filename):
    fp = open(filename, encoding='utf-8')
    arrayOLine = fp.readlines()
    numberOfLines = len(arrayOLine)
    # 初始化特征矩阵
    returnMat = np.zeros((numberOfLines, 7))
    lableVector = []
    index = 0
    for line in arrayOLine:
        line = line.strip()
        listFromline = line.split('\t')
        # 将每列数据填入到特征矩阵中
        returnMat[index, :] = listFromline[0:7]
        # 填入标签
        lableVector.append(listFromline[-1])
        index += 1
    return returnMat, lableVector

"""
数据的归一化处理，将数据归一化到[-1,1]范围
标准化数据
首先是线性标准化算法
方法:
     standardization
参数:
     dataSet:数据集
返回:
     stdDataSet:标准化后的数据
     averageVals:数据每列的平均值矩阵
     ranges:数据每列的标准差矩阵
"""
def standardization(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    averageVals = dataSet.mean(0)
    ranges = maxVals - minVals
    stdDataSet = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]
    stdDataSet = dataSet - np.tile(averageVals, (m, 1))
    stdDataSet = stdDataSet/np.tile(ranges, (m, 1))
    return stdDataSet, averageVals, ranges
"""
kNN算法实现
"""
def kNN(testArry, dataSet, lableVector, k):
    dataSetSize = dataSet.shape[0]
    # 算出欧式距离
    Mat = np.tile(testArry, (dataSetSize, 1)) - dataSet
    sqMat = Mat**2
    sum_sqMat = sqMat.sum(axis=1)
    Mat_distance = sum_sqMat**0.5
    # 排序
    sortIndex = Mat_distance.argsort()
    for i in range(k):
        lable = lableVector[sortIndex[i]]
        print(dataSet[sortIndex[i]])
        print(lable)
