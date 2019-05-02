import numpy as np
import operator

def textFileanalyse(filename):
    fr = open(filename)
    arrayOLine = fr.readlines()
    numberOfLines = len(arrayOLine)
    returnMat = np.zeros((numberOfLines, 3))
    classLableVector = []
    index = 0
    for line in arrayOLine:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLableVector.append(listFromLine[-1])
        index += 1
    return returnMat, classLableVector

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals-minVals
    normDataset = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]
    normDataset = dataSet-np.tile(minVals, (m, 1))
    normDataset = normDataset/np.tile(ranges, (m, 1))
    return normDataset, ranges, minVals

"""
算法实现，
inX-用于分类的数据（测试集）
dataset-用于训练的数据（训练集）
lables-用于分类的标签
k-knn算法的参数，选择距离最小的K个点
"""
def classify(inX, dataSet, lables, k):
    dataSetSize = dataSet.shape[0]
    # 算出欧式距离
    # 二维相减
    diffMat = np.tile(inX, (dataSetSize, 1))-dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    # 开方，算出距离
    distances = sqDistances**0.5
    # 排序
    sortedDistIndex = distances.argsort()
    for i in range(k):
        voteIlable = lables[sortedDistIndex[i]]
        print(voteIlable)
        # classCount[voteIlable] = classCount.get(voteIlable, 0)+1


def testPerson():
    precentTats = float(input("玩游戏"))
    ffMiles = float(input("飞行"))
    iceCream = float(input("冰激淋"))
    filename = '../train/datingTestSet.txt'
    datingDatamat, datingLables = textFileanalyse(filename)
    norDataset, ranges, minVals = autoNorm(datingDatamat)
    # 生成numpy数组
    nyarry = np.array([ffMiles, precentTats, iceCream])
    normarray = (nyarry-minVals)/ranges
    classify(normarray, norDataset, datingLables, 3)

if __name__ == '__main__':
    testPerson()