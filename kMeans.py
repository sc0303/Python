import random
import numpy as np
import recommendations as rd
import classification as cf

blognames, words, data = cf.readFile('D:/machinelearninginaction/PCI_Code Folder/chapter3/blogdata.txt')
# def kCluster(rows, distance = pearson, k = 4):
    ###############确定每个点的最小最大值########################
    # range = [(min([row[i] for row in rows]), max([row[i] for row in rows])) for i in range(len(rows[0]))]


# def kCluster(rows,distance=cf.pearson,k=4):
#     # Determine the minimum and maximum values for each point
#     ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows])) for i in range(len(rows[0]))]
#     print(ranges)
#     # Create k randomly placed centroids
#     clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0]
#     for i in range(len(rows[0]))] for j in range(k)]
#     lastmatches=None
#     for t in range(100):
#         print ('Iteration %d' %t)
#         bestmatches=[[] for i in range(k)]
#         # Find which centroid is the closest for each row
#         for j in range(len(rows)):
#             row=rows[j]
#             bestmatch=0
#             for i in range(k):
#                 d=distance(clusters[i],row)
#                 if d<distance(clusters[bestmatch],row): bestmatch=i
#             bestmatches[bestmatch].append(j)
#         # If the results are the same as last time, this is complete
#         if bestmatches==lastmatches: break
#         lastmatches=bestmatches
#         # Move the centroids to the average of their members
#         for i in range(k):
#             avgs=[0.0]*len(rows[0])
#             if len(bestmatches[i])>0:
#                 for rowid in bestmatches[i]:
#                     for m in range(len(rows[rowid])):
#                         avgs[m]+=rows[rowid][m]
#                 for j in range(len(avgs)):
#                     avgs[j]/=len(bestmatches[i])
#                 clusters[i]=avgs
#     return bestmatches
#
#
# kCluster(data, k = 10)



# dataTmp = np.arange(1,17).reshape(4,4)
dataTmp = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
print(dataTmp)
dataT = ([(min([tmp[i] for tmp in dataTmp]), max([tmp[i] for tmp in dataTmp])) for i in range(len(dataTmp))])#注意这里的列表生成式有两层
print([tmp[1] for tmp in dataTmp])
print(dataT)

