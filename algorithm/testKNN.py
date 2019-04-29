import numpy as np

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

if __name__ == '__main__':
    filename = '../train/datingTestSet.txt'
    datingDatamat, datingLables = textFileanalyse(filename)
    print(datingDatamat)
    print(datingLables)