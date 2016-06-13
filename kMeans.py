import random
import numpy as np
import recommendations as rd
import classification as cf

blognames, words, data = cf.readFile('D:/machinelearninginaction/PCI_Code Folder/chapter3/blogdata.txt')
def kCluster(rows, distance = cf.pearson, k = 4):
    ##############确定每个点的最小最大值########################
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows])) for i in range(len(rows[0]))]###得到每一列的最大最小值

    #############随机创立k个中心点###################
    clusters = [[random.random()*(ranges[i][1] - ranges[i][0]) for i in range(len(rows[0]))] for k in range(k)]###########随机值为何如此设置？

    lastMatch = None
    for i in range(100):
        print('Iteration %d' %i)####不断的重复这个过程，直到找到一个稳态
        bestMatch = [[] for tmp in range(k)]
        for j in range(len(rows)):###############先取出每一行的数据###############
            rowTmp = rows[j]
            bestMatchValue = 0
            for l in range(k):
                d = distance(clusters[l],rowTmp)
                if d < distance(clusters[bestMatchValue],rowTmp): bestMatchValue = l###判断和哪个k值最接近
            bestMatch[bestMatchValue].append(j)######bestMatchValue表示k近邻中的哪一个近邻，j表示第几个数据
        if bestMatch == lastMatch: break
        lastMatch = bestMatch

        ############把中心点移到所有节点的平均位置####################
        for i in range(k):
            avgs = [0.0] * len(rows[0])########################注意这里的用法
            if len(bestMatch[i]) > 0:
                for id in bestMatch[i]:###########取到k份中每份数据对应的行号
                    for m in range(len(rows[id])):#这里之所以用len(rows[id])而不是用len(rows[0])是为了节省效率，因为有的行并不一定全部有数据
                        avgs[m] = avgs[m] + rows[id][m]#####实际上将分到第k组的数据，对应的所有列值相加，这个写法很赞
                for j in range(len(avgs)):
                    avgs[j] = avgs[j] / len(bestMatch[i])
                clusters[i] = avgs
    return bestMatch

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
# print(kCluster(data, k = 10))



# dataTmp = np.arange(1,17).reshape(4,4)
# dataTmp = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
# print(dataTmp)
# dataT = ([(min([tmp[i] for tmp in dataTmp]), max([tmp[i] for tmp in dataTmp])) for i in range(len(dataTmp))])#注意这里的列表生成式有两层
# print([tmp[1] for tmp in dataTmp])
# print(dataT)

# import urllib.request
# from bs4 import BeautifulSoup
# import re
# chare = re.compile(r'[!-\.&]')
# item_owner = {}
# drop_words = ['', '', '', '', '', '', '', '', '', '', '', '']
# current_user = 0
# c = urllib.request.urlopen('http://sports.sina.com.cn/g/euro/2016-06-13/doc-ifxszkzy5178006.shtml')
# soup = BeautifulSoup(c.read(), 'lxml')
# print(soup())
# print(re.sub(chare,' ', str(soup())))
#
# for i in range(1,51):
#     c = urllib.request.urlopen('http://sports.sina.com.cn/g/euro/2016-06-13/doc-ifxszkzy5178006.shtml')
#     soup = BeautifulSoup(c.read(), 'lxml')
#     for td in soup('td'):
#         if('class' in dict(td.attrs) and td['class'] = 'hah'):
#             items = [re.sub(chare,'', a.contents[0].lower()).strip() for a in td('a')]
#             for item in items:
#                 txt = ' '.join([t for t in item.split(' ') if t not in drop_words])
#                 if len(txt) <2:continue
#                 item_owner.setdefault(txt,{})
#                 item_owner[txt][current_user] = 1
#             current_user = current_user + 1
#
#
# c = urllib.request.urlopen('http://sports.sina.com.cn/g/euro/2016-06-13/doc-ifxszkzy5178006.shtml')
# soup = BeautifulSoup(c.read(), 'lxml')
# links = soup('a')
# print(links[10])
# print(soup)

import classification as cf
import math
def scale_down(data, distance = cf.pearson, rate = 0.01):
    n = len(data)
    distance_of_data = [[distance(data[i], data[j]) for i in range(n)] for j in range(n)]
    out_sum = 0.0
    ###给数据随机分配位置坐标
    loc = [[random.random(), random.random()] for i in range(n)]
    fake_list = [[0.0 for j in range(n)] for i in range(n)]
    last_error = None
    for m in range(0, 1000):
        ####计算随机分配位置的数据点之间的距离
        for i in range(n):
            for j in range(n):
                fake_list[i][j] = math.sqrt(sum([pow(loc[i][k]-loc[j][k],2) for k in range(len(loc[i]))]))
        #移动距离
        move = [[0.0, 0.0] for i in range(n)]
        total_error = 0.0
        for k in range(n):
            for l in range(n):
                if l == k: continue
                error_term = (fake_list[l][k] - distance_of_data[l][k])/distance_of_data[l][k]
                move[k][0] += ((loc[k][0] - loc[l][0])/fake_list[l][k])*error_term
                move[k][1] += ((loc[k][1] - loc[l][1])/fake_list[l][k])*error_term
                total_error = total_error + abs(error_term)
        print(total_error)
        if last_error and last_error < total_error:break
        last_error = total_error


        for k in range(n):
            loc[k][0] -= rate * move[k][0]
            loc[k][1] -= rate * move[k][1]

        return loc

from PIL import ImageDraw,Image,ImageFont
def draw_2d(data, labels, jpeg = 'untitled.jpeg'):
    Font = ImageFont.truetype('C:/Windows/winsxs/amd64_microsoft-windows-font-truetype-arial_31bf3856ad364e35_6.1.7601.21733_none_d11c742ddd2959a9/Arial.ttf',51)
    img = Image.new('RGB', (2000, 2000), (255,255,255))
    draw = ImageDraw.Draw(img)
    draw.setfont(Font)
    for i in range(len(data)):
        x = (data[i][0] + 0.5) *1000
        y = (data[i][1] + 0.5)*1000
        draw.text((x,y), labels[i], (0,0,0))
    img.save(jpeg,'jpeg')






blognames,words, data = cf.readFile('D:/machinelearninginaction/PCI_Code Folder/chapter3/zebo.txt')
my_data = scale_down(data)
draw_2d(my_data,words, 'D:/machinelearninginaction/PCI_Code Folder/chapter3/test.jpeg')
