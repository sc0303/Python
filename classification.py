# Write on 2016/06/07 by SunChuan

import re

import feedparser


def getWordCounts(url):
    d = feedparser.parse(url)
    wc = {}
    for key in d.entries:
        if 'summary' in key:
            summary = key.summary
        else:
            summary = key.description
        words = getWords(key.title + '' + summary)
        for word in words:
            # if word not in wc: wc[word] = 0--和下面的一条语句为等价的，但是显然下面的一条语句来的更为简洁
            wc.setdefault(word, 0)
            wc[word] = wc[word] + 1
    return d.feed.title, wc


def getWords(html):
    txt = re.compile(r'<[^>]+>').sub('', html)  #########正则表达式的含义为匹配<括号以内的内容>，其中
    words = re.compile(r'[^A-Z^a-z]+').split(txt)  ############匹配单词的最常用表达式，需要注意的一点是split也是可以使用正则表达式的
    return ([word.lower() for word in words])


#
#
# apcount = {}
# wordCounts = {}
#
# with open('D:/machinelearninginaction/PCI_Code Folder/chapter3/feedlist2.txt') as file:
#     fileIn = [data for data in file]
#     fileLen = len(fileIn)
#     for feedurl in fileIn:
#         title, wc = getWordCounts(feedurl)
#         wordCounts[title] = wc#dict可以外面再叠加一层dict
#         for key, value in wc.items():
#             # if word not in apcount: apcount[word] = 0
#             apcount.setdefault(key, 0)
#             if value > 1:
#                 apcount[key] = apcount[key] + 1
#
#
# wordList = []
# for key, value in apcount.items():
#    frac = float(value) / len(fileIn)
#    if frac < 0.5 or frac > 0.1: wordList.append(key)
#
# with open ('D:/machinelearninginaction/PCI_Code Folder/chapter3/blogdata2.txt', 'w') as file2:
#     file2.write('Blog')
#     for word in wordList:file2.write('\t%s' %word)
#     file2.write('\n')
#     for key, value in wordCounts.items():
#         file2.write(key)
#         for word in wordList:file2.write('\t%d' %wc[word])
#         else:file2.write('\t0')
#     file2.write('\n')
#
# import pandas as pd
#
# df = pd.read_csv('D:/machinelearninginaction/PCI_Code Folder/chapter3/blogdata.txt',sep = '\t', index_col = 'Blog')
# print(df.head(10))
# print(df.index)
# print(df.columns)
# print('hhhhh')

def readFile(fileName):
    file = [line for line in open(fileName)]
    header = file[0].strip().split('\t')
    columns = []
    data = []

    for value in file[1:]:
        line = value.strip().split('\t')
        columns.append(line[0])
        data.append([float(tmp) for tmp in line[1:]])

    return header, columns, data


############计算皮尔逊相关系数######################
from math import sqrt


def pearson(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1Sq = sum([pow(value, 2) for value in v1])
    sum2Sq = sum([pow(value, 2) for value in v2])

    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v2)))
    if den == 0:
        return 0
    return 1.0 - num / den


V1 = []  ####################使用全局变量时需要在方法外先声明全局变量，全局变量应该使用全部大写进行声明
V2 = []


####################聚类方法##################33
class biCluster():
    def __init__(self, vec, left=None, rigth=None, distance=None, id=None):
        self.left = left
        self.right = rigth
        self.distance = distance
        self.id = id
        self.vec = vec


############################聚类方法###############################
def calDistance(rows, distance=pearson):
    distances = {}
    currentDistanctId = -1
    global V1, V2  #################在方法内调用全局变量时需要先使用global关键字声明全局变量

    #############最开始聚类就是数据集中的行####################
    cluster = [biCluster(rows[i], id=i) for i in range(len(rows))]  #######这里生成了对象，注意对象也是可以嵌套在list中使用
    while len(cluster) > 1:
        lowestpair = (0, 1)
        closest = distance(cluster[0].vec, cluster[1].vec)

        # 遍历每一个配对，寻找最小距离
        for i in range(len(cluster)):
            for j in range(i + 1, len(cluster)):
                if (cluster[i].id, cluster[j].id) not in distances:
                    distances[(cluster[i].id, cluster[j].id)] = distance(cluster[i].vec, cluster[
                        j].vec)  ####注意distances的键值是(cluster[i].id, cluster[j].id)
                    d = distance(cluster[i].vec, cluster[j].vec)
                if closest > d:
                    closest = d
                    lowestpair = (i, j)

        ##############计算两个聚类的平均值###################
        mergevec = [(cluster[lowestpair[0]].vec[i] + cluster[lowestpair[1]].vec[i]) / 2 for i in
                    range(len(cluster[lowestpair[0]].vec))]

        #################建立新的聚类############3
        newCluster = biCluster(mergevec, left=cluster[lowestpair[0]], rigth=cluster[lowestpair[1]], distance=closest,
                               id=currentDistanctId)
        currentDistanctId = currentDistanctId - 1
        # print(lowestpair[0], lowestpair[1])
        # print('\n')
        cluster.pop(lowestpair[1])
        cluster.pop(lowestpair[0])  ##############需要注意的是这里面先删除了list后面的元素，然后再删除了list前面的元素，因为删除后面的元素，不会影响前面元素的数值，务必需要注意
        # del cluster[lowestpair[0]]############注意remove,pop, del三者之间的使用区别
        # del cluster[lowestpair[1]]
        cluster.append(newCluster)
    return cluster[0]


def printCluster(cluster, labels=None, n=0):
    for i in range(n):
        tmpFile = open('D:/machinelearninginaction/PCI_Code Folder/chapter3/tmp.txt', 'a')
        tmpFile.write('\t')
        # tmpFile.write('\n')
        tmpFile.close()
    if cluster.id < 0:
        tmpFile = open('D:/machinelearninginaction/PCI_Code Folder/chapter3/tmp.txt', 'a')
        tmpFile.write('-')
        # tmpFile.write('\n')
        tmpFile.close()
        # print('-')
    else:
        tmpFile = open('D:/machinelearninginaction/PCI_Code Folder/chapter3/tmp.txt', 'a')
        if labels == None:
            tmpFile.write(cluster.id)  # print(cluster.id)
            # tmpFile.write('\n')
        else:
            # tmpFile = open ('D:/machinelearninginaction/PCI_Code Folder/chapter3/tmp.txt', 'a')
            tmpFile.write(labels[cluster.id])  # print(labels[cluster.id])
            # tmpFile.close()
        tmpFile.write('\n')
        tmpFile.close()
    if cluster.left != None: printCluster(cluster.left, labels=labels, n=n + 1)
    if cluster.right != None: printCluster(cluster.right, labels=labels, n=n + 1)


from PIL import Image, ImageDraw


def getHeight(cluster):
    if cluster.left == None and cluster.right == None: return 1
    return getHeight(cluster.left) + getHeight(cluster.right)


def getMaxDepth(cluster):
    if cluster.left == None and cluster.right == None: return 0
    return max(getMaxDepth(cluster.left), getMaxDepth(cluster.right)) + cluster.distance


def drawJpg(cluster, labels, jpeg='D:/machinelearninginaction/PCI_Code Folder/chapter3/tmp.jpeg'):
    h = getHeight(cluster)
    w = 1200
    depth = getMaxDepth(cluster)

    scaling = float(w - 150) / depth

    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))
    drawNode = (draw, cluster, 10, (h / 2), scaling, labels)
    img.save(jpeg, 'JPEG')


def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        # Line length
        ll = clust.distance * scaling
        # Vertical line from this cluster to children
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))

        # Horizontal line to left item
        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))

        # Horizontal line to right item
        draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0, 0))

        # Call the function to draw the left and right nodes
        drawnode(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
        drawnode(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)
    else:
        # If this is an endpoint, draw the item label
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))

import pandas as pd
import numpy as np
# def rotateMatrix(data):
#     tmpData = np.zeros(len(data[0]) * len(data))
#     newData = tmpData.reshape(len(data[0]),len(data))
#     print(newData)
#     for i in range(len(data[0])):
#         for j in range(len(data)):
#             newData[j][i] = data[i][j]
#             # newData.append(newRow)
#     return newData

#######################换种写法################################
def rotateMatrix(data):
    newData = []
    for i in range(len(data[0])):
        tmpData = [data[j][i] for j in range(len(data))]
        newData.append(tmpData)
    return newData

# data = np.arange(1,17).reshape(4,4)
#
# print(data)
# print(rotateMatrix(data))







# blognames, words, data = readFile('D:/machinelearninginaction/PCI_Code Folder/chapter3/blogdata.txt')
# cluster = calDistance(data, pearson)
# printCluster(cluster, labels = words)
# print(getHeight(cluster))
# print(getMaxDepth(cluster))
# drawJpg(cluster, labels=blognames, jpeg='D:/machinelearninginaction/PCI_Code Folder/chapter3/tmp.jpeg')
