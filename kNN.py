# import numpy as np
# import pandas as pd
# import operator as op
# import matplotlib.pyplot as plt
# import os
# import string
# from math import log
#
#
# def createDataset():
#     group = np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
#     labels = ['A','A','B','B']
#     return group,labels
#
# ###############数据读入#####################
# def file2matrix(filename):
#     fr = open(filename)
#     arrayOfLines = fr.readlines()
#     numberOfLines = len(arrayOfLines)
#     returnMat = np.zeros((numberOfLines,3))
#     classLabelVector = []
#     index = 0
#     for line in arrayOfLines:
#         line = line.strip() ##去掉前后空格
#         listFromLine = line.split('\t')
#         returnMat[index,:] = listFromLine[0:3]
#         if listFromLine[-1] == 'largeDoses':
#             classLabelVector.append(3)
#         elif listFromLine[-1] == 'smallDoses':
#             classLabelVector.append(2)
#         else:
#             classLabelVector.append(1)
#         # classLabelVector.append(lambda listFromLine[-1]: )
#         index = index + 1
#     return returnMat,classLabelVector
#
# #############################数据归一化##############################
# def autoNorm(dataSet):
#     minVals = dataSet.min()
#     maxVals = dataSet.max()
#     ranges = maxVals - minVals
#     # print(np.shape(dataSet))
#     normDataSet = np.zeros(np.shape(dataSet))
#     m = dataSet.shape[0]
#     print(dataSet.shape[0],dataSet.shape[1])
#     normDataSet = dataSet - np.tile(minVals, (m,1))
#     normDataSet = normDataSet/np.tile(ranges,(m,1))
#     return  normDataSet, ranges, minVals
#
#
# def datingClassTest():
#     hRatio = 0.1
#     datingDataMat, datingLabels = file2matrix('D:/machinelearninginaction/Ch02/datingTestSet.txt')
#     normMat, ranges, minValues = autoNorm(datingDataMat)
#     m = normMat.shape[0]
#     numTestVecs = int(m*hRatio)
#     errorCount = 0
#     for i in range(numTestVecs):
#         # classResults = classify0(normData[i,:],normMat[numTestVecs:m,:]),datingLabels[numTestVecs:m],3)# 输入了训练集和测试集
#         print('the classifier came back with：the real answer is: %d' %datingLabels[i])
#         # if classResults != datingLabels[i]:
#         #     errorCount = errorCount + 1
#         print('the total error rate is: %f' %(errorCount / float(numTestVecs)))
#
#
# ########################k近邻识别手写数据字符##############################
# #########################将二维数据转变成一维数组##########################
# def img2Vector(filename):
#     returnVector = np.zeros((1,1024))
#     with open(filename) as f:
#         for i in np.arange(32):
#             line = f.readline()
#             line_list = list(line)
#             newArray = np.array(line_list)
#             returnVector[0, i * 32 : i * 32 + 31] = newArray[0:31]
#     return returnVector
#
#
#
# ######################测试结果准确率###########################
# def handWritingTest():
#     result = []
#     fileList = os.listdir('D:/machinelearninginaction/Ch02/digits/trainingDigits')###########列出目录下的所有文件名
#     fileNum = len(fileList)
#     m = np.zeros((fileNum,1024))
#     for i in range(fileNum):
#         result.append(fileList[i].split('.')[0].split('_')[0])
#         m[i,:] = img2Vector('D:/machinelearninginaction/Ch02/digits/trainingDigits/%s' %fileList[i])
#     df = pd.DataFrame(m)
#     testFile = os.listdir('D:/machinelearninginaction/Ch02/digits/testDigits')
#     testFileNum = len(testFile)
#     errCount = 0
#     for i in range(testFileNum):
#         actResult = testFile[i].split('.')[0].split('_')[0]
#         vectorInput = img2Vector('D:/machinelearninginaction/Ch02/digits/trainingDigits/%s' %testFile[i])
#         preResult = classify0(vectorInput,m,result,3)
#         if preResult == actResult:
#             print('The result is right')
#         else:
#             errCount = errCount + 1
#             print('The result is wrong and the right result is %d' %preResult)
#     print('the prediction ration is %s' %(errCount/testFileNum))
#     print(len(fileList))
#
# # handWritingTest()
#
# ##################################决策树################################
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # print(len(img2Vector('D:/machinelearninginaction/Ch02/digits/testDigits/0_0.txt')))
#
#
#
#
#
# # datingClassTest()
# # datingData, datinglabels = file2matrix('D:/machinelearninginaction/Ch02/datingTestSet.txt')
# # normData = autoNorm(datingData)
# # print(normData)
# # print(datingData)
# # fig = plt.figure()
# # ax1 = fig.add_subplot(1,2,1)
# # ax2 = fig.add_subplot(1,2,2)
# # # print(np.array(datinglabels))
# # ax1.scatter(datingData[:,1],datingData[:,2],15.0 * np.array(datinglabels), 15.0 * np.array(datinglabels))
# # # ax2.scatter(normData[:,1],normData[:,2])
# # plt.show()




from numpy import *
import operator
from os import listdir

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

group, labels = createDataSet()
print(classify0([0,0], group,labels, 3))