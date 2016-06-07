# write by sunchuan on 2016/06/01
import pandas as pd

my_data = [['slashdot', 'USA', 'yes', 18, 'None'],
           ['google', 'France', 'yes', 23, 'Premium'],
           ['digg', 'USA', 'yes', 24, 'Basic'],
           ['kiwitobes', 'France', 'yes', 23, 'Basic'],
           ['google', 'UK', 'no', 21, 'Premium'],
           ['(direct)', 'New Zealand', 'no', 12, 'None'],
           ['(direct)', 'UK', 'no', 21, 'Basic'],
           ['google', 'USA', 'no', 24, 'Premium'],
           ['slashdot', 'France', 'yes', 19, 'None'],
           ['digg', 'USA', 'no', 18, 'None'],
           ['google', 'UK', 'no', 18, 'None'],
           ['kiwitobes', 'UK', 'no', 19, 'None'],
           ['digg', 'New Zealand', 'yes', 12, 'Basic'],
           ['slashdot', 'UK', 'no', 21, 'None'],
           ['google', 'UK', 'yes', 18, 'Basic'],
           ['kiwitobes', 'France', 'yes', 19, 'Basic']]

#write the file to the excel
# df = pd.DataFrame(my_data)
# try:
#     df.to_excel('D:/myData.xlsx', index=False, header=False)  # except:
# except:
#     print('Wrong location')


# 需要非常注意的一点是，在类中如果定义变量如果不加self，表示是类的一个属性（可以通过“类名.变量名”的方式引用），加了表示是类的实例的一个属性（可以通过“实例名.变量名”的方式引用）。
# 例子如下：
# class test(object):
#     val = 1
#     def __init__(self):
#         self.val = 2
# myTest = test()
# print(myTest.val)#访问self定义的实例的属性
# print(test.val)#访问未使用self定义的类的局部变量
# 这也是为什么__init__方法的第一个参数必须为self的原因，因为__init__参数中定义的都是方法的属性，而不是类的属性

# 在python2中是否添加(object)是有区别的，在python中是否写(object)是没有区别的，因为在python3中默认调用的就是object基类
class decisionNode(object):
    # col表示输入条件，value表示判断条件，tb和fb表示输出的对应子节点
    # 类内部上来就定义__init__函数的目的是为了？
    # 注意到__init__方法的第一个参数永远是self，表示创建的实例本身，因此，在__init__方法内部，就可以把各种属性绑定到self，因为self就指向创建的实例本身。
    # 有了__init__方法，在创建实例的时候，就不能传入空的参数了，必须传入与__init__方法匹配的参数，但self不需要传，Python解释器自己会把实例变量传进去：
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col
        self.vaule = value
        self.results = results
        self.tb = tb
        self.fb = fb

    # 数据分割，这个函数的写法还是蛮有技术含量的
    # 和普通的函数相比，在类中定义的函数只有一点不同，就是第一个参数永远是实例变量self，并且，调用时，不用传递该参数。除此之外，类的方法和普通函数没有什么区别，所以，你仍然可以用默认参数、可变参数、关键字参数和命名关键字参数。
    def divideData(self, rows, column, value):
        splitFunction = None
        if isinstance(value, int) or isinstance(value, float):
            splitFunction = lambda row: row[column] >= value  # 对函数可以进行赋值
        else:
            splitFunction = lambda row: row[column] == value
        set1 = [row for row in rows if splitFunction(row)]  # 注意if之后的逻辑是用来判断是否满足条件，取满足条件的那一部分
        set2 = [row for row in rows if not splitFunction(row)]  # 取不满足条件的那一部分
        return set1, set2

    # print(divideData(my_data,2,'yes'))

    def uniqueResults(self, rows):
        results = {}
        for row in rows:
            r = row[len(row) - 1]  # 取一行最后一个元素，基本的使用方法需要多学习，多看code
            if r not in results: results[r] = 0
            results[r] = results[r] + 1
        return results

    def giniImpurity(self, rows):
        imp = 0
        num = len(rows)
        counts = self.uniqueResults(rows)
        for k1 in counts:
            p1 = float(counts[k1]) / num
            for k2 in counts:
                if k1 == k2: continue  # 注意学习这种将if后面只有一条语句写在和if一行的写法
                p2 = float(counts[k2]) / num
                imp = imp + p1 * p2
        return imp

    def giniimpurity(self, rows):
        total = len(rows)
        counts = self.uniqueResults(rows)
        imp = 0
        for k1 in counts:
            p1 = float(counts[k1]) / total
            for k2 in counts:
                if k1 == k2: continue
                p2 = float(counts[k2]) / total
                imp += p1 * p2
        return imp

    def entropy(self, rows):
        from math import log
        log2 = lambda x: log(x) / log(2)
        results = self.uniqueResults(rows)
        ent = 0
        for r in results:
            p = float(results[r]) / len(rows)
            ent = ent - p * log2(p)
        return ent

    def test(self):
        # print(self.uniqueResults(my_data))
        # print(self.entropy(my_data))
        self.set1, self.set2 = self.divideData(my_data, 2, 'yes')
        # print(self.set1)
        # print(self.set2)
        # print(self.entropy(self.set1))
        # print(self.entropy(self.set2))
        # self.buildTree(my_data, self.entropy)

    def buildTree(self, rows, scoref):
        if len(rows) == 0: return decisionNode
        currentScore = scoref(rows)
        bestGain = 0
        bestCriteria = None
        bestSets = None
        # 列数
        colunmCounts = len(rows[0]) - 1
        for i in range(colunmCounts):
            colunmVaules = {}
            for row in rows:
                colunmVaules[row[i]] = 1

            for value in colunmVaules:
                (set1, set2) = self.divideData(rows, i, value)
                p = float(len(set1)) / len(rows)
                gain = currentScore - p * scoref(set1) - (1 - p) * scoref(set2)
                if gain > bestGain and len(set1) > 0 and len(set2) > 0:
                    bestGain = gain
                    bestCriteria = (i, value)
                    bestSets = (set1, set2)

            if bestGain > 0:
                trueBranch = self.buildTree(bestSets[0], self.entropy)
                falseBranch = self.buildTree(bestSets[1], self.entropy)
                return decisionNode(col=bestCriteria, value=bestCriteria[1], tb=trueBranch, fb=falseBranch)

            else:
                return decisionNode(results=self.uniqueResults(rows))




# import xml.dom.minidom
# import urllib.request
# import os
# zwskey="YOUR API KEY"
#
#
# def getAddress(address, city):
#     addressTmp = address.replace(' ', '+')
#     url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
#     url = url + 'zws-id=%s&address=%s&citystatezip=%s' %(zwskey,addressTmp,city)
#     print(url)
#     doc = xml.dom.minidom.parseString(urllib.request.urlopen(url).read())
#     print(doc)
#
#
# def getPriceList():
#     list = []
#     with open('D:/machinelearninginaction/PCI_Code Folder/chapter7/addresslist.txt') as file:
#         # print(file.readlines())
#         for line in file.readlines():#这里面file.readlines()效果等同于readline(),原因是readline()是读取了文件中的所有行
#             tmpData = getAddress(line.strip(),'Cambridge, MA')
#             list.append(tmpData)
#         print(list)
#         return list
#
# def getpricelist():
#     l1=[]
#     with open('D:/machinelearninginaction/PCI_Code Folder/chapter7/addresslist.txt') as file:
#         for line in file:
#             data=getaddressdata(line.strip(),'Cambridge,MA')
#             l1.append(data)
#         return l1

import urllib.request
import xml.dom.minidom

apiKey='470NUNJHETN'
def getRandomRating(c):
    url = "http://services.hotornot.com/rest/?app_key=%s" %apiKey
    url = url + "&method=Rate.getRandomProfile&retrieve_num=%d" % c
    url = url + "&get_rate_info=true&meet_users_only=true"
    mes = urllib.request.urlopen(url).read()
    doc = xml.dom.minidom.parseString(mes)
    print(doc)
    emids = doc.getElementsByTagName('emid')
    ratings = doc.getElementsByTagName('rating')
    result = []
    for e, r in zip(emids, ratings):
        if r.firstChild != None:
            result.append(e.firstChild.data, r.firstChild.data)
        return result
stateregions={'New England':['ct','mn','ma','nh','ri','vt'],
              'Mid Atlantic':['de','md','nj','ny','pa'],
              'South':['al','ak','fl','ga','ky','la','ms','mo',
                       'nc','sc','tn','va','wv'],
              'Midwest':['il','in','ia','ks','mi','ne','nd','oh','sd','wi'],
              'West':['ak','ca','co','hi','id','mt','nv','or','ut','wa','wy']}

def getPeopleData(ratings):
    result = []


def getpeopledata(ratings):
  result=[]
  for emid,rating in ratings:
    # URL for the MeetMe.getProfile method
    url="http://services.hotornot.com/rest/?app_key=%s" % api_key
    url+="&method=MeetMe.getProfile&emid=%s&get_keywords=true" % emid

    # Get all the info about this person
    try:
      rating=int(float(rating)+0.5)
      doc2=xml.dom.minidom.parseString(urllib2.urlopen(url).read())
      gender=doc2.getElementsByTagName('gender')[0].firstChild.data
      age=doc2.getElementsByTagName('age')[0].firstChild.data
      loc=doc2.getElementsByTagName('location')[0].firstChild.data[0:2]

      # Convert state to region
      for r,s in stateregions.items():
        if loc in s: region=r

      if region!=None:
        result.append((gender,int(age),region,rating))
    except:
      pass
  return result


def taobao2(keyWord):
    result = []
    url = "https://s.2.taobao.com/list/list.htm?q=%s&search_type=item&app=shopsearch" %keyWord
    print(url)
    doc = urllib.request.urlopen(url).read()
    print(doc)





def getrandomratings(c):
  # Construct URL for getRandomProfile
  url="http://services.hotornot.com/rest/?app_key=%s" % api_key
  url+="&method=Rate.getRandomProfile&retrieve_num=%d" % c
  url+="&get_rate_info=true&meet_users_only=true"

  f1=urllib2.urlopen(url).read()

  doc=xml.dom.minidom.parseString(f1)

  emids=doc.getElementsByTagName('emid')
  ratings=doc.getElementsByTagName('rating')

  # Combine the emids and ratings together into a list
  result=[]
  for e,r in zip(emids,ratings):
    if r.firstChild!=None:
      result.append((e.firstChild.data,r.firstChild.data))
  return result

stateregions={'New England':['ct','mn','ma','nh','ri','vt'],
              'Mid Atlantic':['de','md','nj','ny','pa'],
              'South':['al','ak','fl','ga','ky','la','ms','mo',
                       'nc','sc','tn','va','wv'],
              'Midwest':['il','in','ia','ks','mi','ne','nd','oh','sd','wi'],
              'West':['ak','ca','co','hi','id','mt','nv','or','ut','wa','wy']}






# myDecionNode = decisionNode()
# myDecionNode.test()
# getRandomRating(500)
taobao2('k3003')





