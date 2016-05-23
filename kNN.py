import numpy as np
import operator as op
import matplotlib.pyplot as plt
import os
def createDataset():
    group = np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

def file2matrix(filename):
    fr = open(filename)
    arrayOfLines = fr.readlines()
    numberOfLines = len(arrayOfLines)
    returnMat = np.zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOfLines:
        line = line.strip() ##去掉前后空格
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index = index + 1
    return returnMat,classLabelVector

myfile = file2matrix('D:/machinelearninginaction/Ch02/datingTestSet.txt')

print(myfile)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter()


print(np.zeros((5,3)))






myData = createDataset()
print(myData)