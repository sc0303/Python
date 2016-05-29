import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import log
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.externals.six import StringIO
import pydot
# #########################计算熵指#####################33
# def calcShannonEnt(dataset):
#     dataLen = len(dataset)
#     labelCounts = {}
#     for vec in dataset:
#         currentValue = str(vec[-1])
#         if currentValue not in labelCounts:
#             labelCounts[currentValue] = 0
#         labelCounts[currentValue] = labelCounts[currentValue] + 1
#
#     shannoEnt = 0
#     for key in labelCounts:
#         pro = float(labelCounts[key]) / dataLen
#         shannoEnt = shannoEnt - pro * log(pro, 2)
#     return shannoEnt
#
#
# #############################创建dataset#################
# def createDataSet():
#     dataSet = [['1', '1', 'yes'], ['1', '0', 'no'], ['1', '1', 'yes'], ['0', '1', 'no'], ['0', '1', 'no']]
#     labels = ['no surfacing', 'flippers']
#
#     return dataSet, labels
#
#
# ############################分割数据####################
# def splitData(dataSet, axis, value):
#     resultData = []
#     for vector in dataSet:
#         if vector[axis] == value:
#             reducedVector = vector[:axis]
#             reducedVector.extend(vector[axis + 1:])
#             resultData.append(reducedVector)
#     return resultData
#
#
#########################挑选最大的熵值#########################
def chooseBest(dataSet):
    numFeatures = len(dataSet[0]) - 1
    bestEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]  #############注意这里面列表生成式的使用方式
        uniqueValues = set(featList)
        newEntropy = 0
        for value in uniqueValues:
            subDataSet = splitData(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy = newEntropy + prob * calcShannonEnt(dataSet)
        infoGain = bestEntropy - newEntropy
        bestFeature = i
    return bestFeature


######################创建绘图###########################
# decisionNode = dict(boxstyle="sawtooth", fc="0.8")
# leafNode = dict(boxstyle="round4", fc="0.8")
# arrow_args = dict(arrowstyle="<-")
#
#
# def plotNode(nodeTxt, centerPt, parentPt, nodeType):
#     plt.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
#                  xytext=centerPt, textcoords='axes fraction',
#                  va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)
#
#
def createPlot():
    fig = plt.figure(1,facecolor='white')
    fig.clf()
    # ax1 = plt.subplots(111,frameon = 'false')
    plotNode('a decision node', (0.5, 0.1),(0.1, 0.5),decisionNode)
    plotNode('a leaf node',(0.8, 0.1),(0.3, 0.8),leafNode)
    plt.show()
#
# createPlot()

def readFile(dateSet):
    with open(dateSet) as f:
        frTmp = f.readlines()
        fr = [lineTmp.strip().split('\t') for lineTmp in frTmp]
        frInput = [frInputTmp[0:3] for frInputTmp in fr]
        frOutput = [frOutputTmp[4:] for frOutputTmp in fr]
        return frInput, frOutput

input, output = readFile('C:/Users/Alance/PycharmProjects/machinelearninginaction/Ch03/lenses.txt')
iris = load_iris()
myClf = tree.DecisionTreeClassifier()
myClf.fit(iris.data, iris.target)
data = StringIO()
tree.export_graphviz(myClf,out_file = data)
print(data.getvalue())
graph = pydot.graph_from_dot_data(data.getvalue())
graph.write_pdf('C:/Users/Alance/PycharmProjects/machinelearninginaction/Ch03/dt.pdf')
# myData, myLabels = createDataSet()
#
# print(chooseBest(myData))




# print(splitData(myData,1,'1'))


# print(calcShannonEnt(myData))
