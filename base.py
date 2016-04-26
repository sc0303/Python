# Coding by SunChuan in 2016/04/06
import os
import xlrd, xlwt
import csv
import pandas as pd
from collections import Iterable
from collections import Iterator
from types import MethodType
import pickle
import json
import re

# a.next()和next(a)的区别, line173是否解释了这个问题？
# 所以是凡方法中带有__func__方法的，都可以通过func(a)的形式调用，而不需要使用a.func()的形式进行调用

# # 地板除法两个整数的除法仍然是整数：
# print(10//3)
#
# # 在计算机内存中，统一使用Unicode编码，当需要保存到硬盘或者需要传输的时候，就转换为UTF-8编码。
# print('The quick brown fox','jumps over','the lazy dog')
#
# classmates = ['Michael', 'Bob', 'Tracy']
# print(len(classmates))
# classmates.append('sunchuan')#list中使用append进行添加元素
# list1 = classmates
# list1.insert(1, 'sunchuan')#list中使用insert进行插入元素
# print(list1)
# list1.pop(1) #使用pop删除元素
# print(list1)
#
# # 无论list还是tuple，调用的是有都使用[]进行调用，包括切片的调用也是如此
# age = 3
# if age >= 18:
#     print('adult')
# elif age >= 6:
#     print('teenager')
# else:
#     print('kid')
#
# #字典，字典是无序的,字典中的key不能重复,如果key重复，可能会取其中一个value
# d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
# print(d)
# print(d['Michael'])
# print(d.get('Michael'))#判断是否存在Michael
# pop = d.pop('Michael')#删除字典中的key-value
# print(d)
#
# #set 注意set中不可以有重复数据
# s = set([1,2,3,4,2])
# print(s)
# s.add(10)#添加元素
# print(s)
# s.remove(10)#删除元素
# print(s)

# ###############################################函数###################################################
# #函数名其实就是指向一个函数对象的引用，完全可以把函数名赋给一个变量，相当于给这个函数起了一个“别名”：
# a = abs # 变量a指向abs函数
# print(a(-1))
# #如果没有return语句，函数执行完毕后也会返回结果，只是结果为None,return None可以简写为return。
# def my_abs(x):
#     if x >= 0:
#         return x
#     else:
#         return -x
# print(my_abs(-1))
# #函数可以返回多个数值的原因为返回值是一个tuple！但是，在语法上，返回一个tuple可以省略括号，而多个变量可以同时接收一个tuple，按位置赋给对应的值，所以，Python的函数返回多值其实就是返回一个tuple，但写起来更方便。
# ###############对函数添加默认参数
# def enroll(name, gender, age=6, city='Beijing'):
#     print('name:', name)
#     print('gender:', gender)
#     print('age:', age)
#     print('city:', city)
#
#
# #####################默认参数######################
# def calc(*nums):
#     sum = 0
#     for i in nums:
#         sum = sum + i
#     return sum
#
# list = [1,2,3,4]
# tuple = (1,2,3,4,5)
# print(calc(*list))
# print(calc(*tuple))
#
# ####################关键字参数###########################
# #可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。而关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict。
# def person(name, age, **kw):
#     print('name:', name, 'age:', age, 'other:', kw)
# extra = {'city': 'Beijing', 'job': 'Engineer'}
# print(person('Jack', 24, **extra))
#
#
# ##############命名关键字参数#########################
# #和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数,参数传入时，传入的参数名称必须传出参数，且参数名需要等同于已经命名的参数，否则会报错
# def person(name, age, *,city, job):
#     print('name:', name, 'age:', age, 'city', city, 'job', job)
# extra2 = {'city': 'Beijing', 'job': 'Engineer'}
# print(person('Jack', 24, **extra2))
#
# #####################默认参数、关键字参数、命名关键字参数为理解重点########################
#
# ##########很常用的一种使用方式，列表生成式,注意列表生成器一定要中括号括起来###############################
# print([x * x for x in range(1,10)])
# print([x * x for x in range(1,10) if x % 2 ==0])
# print([x + y for x in 'xyz' for y in 'abc'])
#
# ####################生成器####################
# ############将生成式的中括号改成圆括号即可变成生成器######
# print((x * x for x in range(1,10)))
# g = (x * x for x in range(1,10))
# print(next(g))
# #########生成器还有一种定义方式，就是函数中使用关键一yield关键字generator和函数的执行流程不一样。函数是顺序执行，遇到return语句或者最后一行函数语句就返回。而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。
#
# ####################迭代器#################################
# # 这些可以直接作用于for循环的对象统称为可迭代对象：Iterable。
# # 可以使用isinstance()判断一个对象是否是Iterable对象：
# print(isinstance([], Iterable))
# # 可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。
# # 可以使用isinstance()判断一个对象是否是Iterator对象：
# print(isinstance([], Iterator))
# # 注意理解生成器和迭代器的区别，生成器是迭代器的真子集
#
# #################函数式编程###############
# # 函数式编程函数式编程的一个特点就是，允许把函数本身作为参数传入另一个函数，还允许返回一个函数！
# # Python对函数式编程提供部分支持。由于Python允许使用变量，因此，Python不是纯函数式编程语言。
# # 函数名其实就是指向函数的变量！对于abs()这个函数，完全可以把函数名abs看成变量，它指向一个可以计算绝对值的函数！
# # 既然变量可以指向函数，函数的参数能接收变量，那么一个函数就可以接收另一个函数作为参数，这种函数就称之为高阶函数。
# def add(x, y, f):
#     return f(x)+ f(y)
# print(add(-3, 5, abs))
###############map() reduce() sorted() filter()的使用##################
# 闭包的使用，闭包理解起来比较困难
# 匿名函数的好处是没有函数名，不存在函数名冲突的情况
# print(list(map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9])))

# 这种在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator），本质上，decorator就是一个返回函数的高阶函数。
# 装饰器没有看懂
# def log(func):
#     def warpper(*args, **kw):
#         print ('call % s():' %func.__name__)
#         return func(*args, **kw)
#     return warpper
#
# @log
# def now():
#     print('test')
#
# now()



# 偏函数
# 简单总结functools.partial的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单。

# 作用域
# 类似_xxx和__xxx这样的函数或变量就是非公开的（private），不应该被直接引用，比如_abc，__abc等；
# _下划线这样的实例变量外部是可以访问的，但是，按照约定俗成的规定，当你看到这样的变量时，意思就是，“虽然我可以被访问，但是，请把我视为私有变量，不要随意访问”。
# 双下划线开头的实例变量是不是一定不能从外部访问呢？其实也不是。不能直接访问__name是因为Python解释器对外把__name变量改成了_Student__name，所以，仍然可以通过_Student__name来访问__name变量：
# 两侧都有下划线的变量是系统默认的变量

# 面向对象编程
# 和静态语言不同，Python允许对实例变量绑定任何数据，也就是说，对于两个实例变量，虽然它们都是同一个类的不同实例，但拥有的变量名称都可能不同：
# bart = Student('Bart Simpson', 59)
# lisa = Student('Lisa Simpson', 87)
# bart.age = 8
# bart.age
# lisa.age
# 即除了student原先定义的name和age属性，可以再重新定义age数字你个，皆可以对实例变量绑定任何数据，同时注意实例属性和类属性的区别，在类中直接定义的属性叫类属性，类属性一定不要和实例属性重合了
# 系统会优先访问实例的属性再访问类的属性
# 访问限制
# 如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线__，在Python中，实例的变量名如果以__开头，就变成了一个私有变量（private），只有内部可以访问，外部不能访问

# # 使用dir可以获得对象的所有属性和方法
# print(dir('str'))
#
#
# # 类似__xxx__的属性和方法在Python中都是有特殊用途的，比如__len__方法返回长度。在Python中，如果你调用len()函数试图获取一个对象的长度，实际上，在len()函数内部，它自动去调用该对象的__len__()方法，所以，下面的代码是等价的：
# # 我们自己写的类，如果也想用len(myObj)的话，就自己写一个__len__()方法：
# class MyDog(object):
#     def __len__(self):
#         return 100
#     def len(self):
#         return 200
# 注意hasattr,getattr,setattr的使用方法
# dog = MyDog()
# print(dog.__len__())
# print(len(dog))
# print(dog.len())

# class Student(object):
#     pass
#
# # s = Student()
#
#
# def set_score(self, score):
#     self.score = score


# 实例可以绑定属性、方法、类也可以绑定属性、方法
# s.set_score = MethodType(set_score,s)#给实例动态绑定方法（需要借助MethodType），但是给一个实例绑定方法对另外一个实例是不起作用的，为了给所有实例都绑定方法，可以给class类绑定方法
# print(s.set_score(100))
# print(s.score)

# s1 = Student()
# Student.set_score = set_score
# s1.set_score(100)
# print(s1.score)
# 通常情况下，上面的set_score方法可以直接定义在class中，但动态绑定允许我们在程序运行的过程中动态给class加上功能，这在静态语言中很难实现。
####################################__slots__##############################
# 但是，如果我们想要限制实例的属性怎么办？比如，只允许对Student实例添加name和age属性。
# 为了达到限制的目的，Python允许在定义class的时候，定义一个特殊的__slots__变量，来限制该class实例能添加的属性：
# class Student(object):
#     __slots__ = ('name', 'age')
#
# s = Student()
# s.name = 'sunchuan'
# print(s.name)
# s.score = '100'
# print(s.score)#__slots__限制了score绑定属性只可以为name和age
# # 使用__slots__要注意，__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的：

# 对于类的方法，装饰器一样起作用。Python内置的@property装饰器就是负责把一个方法变成属性调用的：
# 没有太理解

# type()动态语言和静态语言最大的不同，就是函数和类的定义，不是编译时定义的，而是运行时动态创建的。
# type()函数既可以返回一个对象的类型，又可以创建出新的类型，比如，我们可以通过type()函数创建出Hello类，而无需通过class Hello(object)...的定义：
# def fn(self, name='world'): # 先定义函数
#     print('Hello, %s.' % name)
# Hello = type('Hello', (object,), dict(hello=fn)) # 创建Hello class
# 创建一个class对象，type()函数依次传入3个参数：
# class的名称；
# 继承的父类集合，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法；
# class的方法名称与函数绑定，这里我们把函数fn绑定到方法名hello上。
#############错误处理###########################

# try:
#     print('try...')
#     r = 10 / int('2')
#     print('result:', r)
# except ValueError as e:
#     print('ValueError:', e)
# except ZeroDivisionError as e:
#     print('ZeroDivisionError:', e)
# else:
#     print('no error!')
# finally:
#     print('finally...')
# print('END')

# finally之后的语句一定会执行
# raise语句如果不带参数，就会把当前错误原样抛出。
# 此外，在except中raise一个Error，还可以把一种类型的错误转化成另一种类型：
# 只要是合理的转换逻辑就可以，但是，决不应该把一个IOError转换成毫不相干的ValueError。
# logging为调试的终极武器

###################################文件读写############################
# try:
#     f = open('C:/Users/Alance/Desktop/需求/报表割接/二维码新脚本.sql', 'r')#还可以在括号中添加文件的编码格式
#     print(f.read())
# finally:
#     f.close()
#########为了简便写法，上述可以写生###########
#
# with open('C:/Users/Alance/Desktop/需求/报表割接/二维码新脚本.sql', 'r') as f:
#     print(f.read())
# #上述写法的好处是不需要f.close()来确保数据读完之后的关闭。

##############对文件进行一行行读取##################
# with open('C:/Users/Alance/Desktop/需求/报表割接/二维码新脚本.sql', 'r') as f:
#     for line in f.readlines():
#         print(line.strip())
# 同样对于文件的写入也要实用上述with as的格式，需要养成良好的读写习惯。

# 操作文件与目录中提供了一些常用的函数，需要熟悉实用
# 常用函数如下：
# print(os.name)
# print(os.environ)
# print(os.environ.get('PATH'))
# print(os.path.abspath())
# print(os.path.join('/Users/michael', 'testdir'))
# os.mkdir('/Users/michael/testdir')
# os.rmdir('/Users/michael/testdir')
# os.path.split('/Users/michael/testdir/file.txt')#拆分文件和路径
# os.path.splitext('/Users/michael/testdir/file.txt')#拆分文件扩展名
# os.rename('test.txt','test.py')
# os.remove('test.py')
# [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']#列出所有的.py文件
# 我们把变量从内存中变成可存储或传输的过程称之为序列化，在Python中叫pickling，在其他语言中也被称之为serialization，marshalling，flattening等等，都是一个意思。
# pickle.dumps()
# pickle.load()
# json.dumps()
# json.loads()
##########################正则表达式##################################
# \d 用来匹配一个数字
# \w用来匹配一个字母或者数字
# .可以匹配任意字符
# \s表示空格
# *表示任意个字符（包括0个），+表示至少一个字符，？表示0或者1个字符，{n}表示n个字符，{n,m}表示n-m个字符
# 为了更精准的匹配，可以使用[]进行匹配
# [0-9a-zA-Z\_]可以匹配一个数字、字母或者下划线
# [a-zA-Z\_][0-9a-zA-Z\_]*可以匹配由字母或下划线开头，后接任意个由一个数字、字母或者下划线组成的字符串，也就是Python合法的变量；
# [a-zA-Z\_][0-9a-zA-Z\_]{0, 19}更精确地限制了变量的长度是1-20个字符（前面1个字符+后面最多19个字符）。
# A|B可以匹配A或B，所以[P|p]ython可以匹配'Python'或者'python'。
# ^表示行的开头，^\d表示必须以数字开头。
# $表示行的结束，\d$表示必须以数字结束。
# test = '用户输入'
# if re.match(r'\c{3}\-\d{3,8}',test):
#     print('ok')
# elif:
#     print('failed')
#######正则表达式用于分词
# print(re.split(r'\s+','a b   c'))
# m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')############正则表达式可以进行分组
# print(m.group())
# print(m.group(0))
# print(m.group(1))
# 最后需要特别指出的是，正则匹配默认是贪婪匹配，也就是匹配尽可能多的字符

line = 0
dict_area = {'安徽省': 0,
             '北京市': 0,
             '福建省': 0,
             '甘肃省': 0,
             '广东省': 0,
             '广西壮族自治区': 0,
             '贵州省': 0,
             '海南省': 0,
             '河北省': 0,
             '河南省': 0,
             '黑龙江省': 0,
             '湖北省': 0,
             '湖南省': 0,
             '吉林省': 0,
             '江苏省': 0,
             '江西省': 0,
             '辽宁省': 0,
             '内蒙古自治区': 0,
             '宁夏回族自治区': 0,
             '青海省': 0,
             '山东省': 0,
             '山西省': 0,
             '陕西省': 0,
             '上海市': 0,
             '四川省': 0,
             '天津市': 0,
             '西藏自治区': 0,
             '新疆维吾尔自治区': 0,
             '云南省': 0,
             '浙江省': 0,
             '重庆市': 0}



# csvfile = open('C:/Users/Alance/PycharmProjects/Python/2.csv','wb')
# writer = csv.writer(csvfile)

# list =[][]
# df = pd.DataFrame()
#
#
# with open('C:/Users/Alance/PycharmProjects/Python/1.csv') as f:
#     reader = csv.reader(f)
#     for line in reader:
#         if line[0] in dict_area and dict_area.get(line[0]) <= 99:
#             list.append(line)
#             print(line)
#             dict_area.
#             dict_area(line[0]) = 1
#             dict_area[line[0]] = dict_area[line[0]] + 1
#             print(line)
#             print(pd.DataFrame(line))
#             df.append(pd.DataFrame(line))
            # print(df)
# print(df)

# df = pd.DataFrame(line)
# df.to_csv('C:/Users/Alance/PycharmProjects/Python/2.csv')
# csvfile.close()




#
#     while line < 10:
#         print(next(reader))
#         line = line + 1



# csvfile = open('C:/Users/Alance/PycharmProjects/Python/data1.csv', 'rb')
# reader = csv.reader(csvfile)
# i = 0
# for line in reader:
#     if i == 0:
#         print(line)
#         i = i + 1
#     csvfile.close()


















# print(table.nrows)
# i = 0;
# while i < table.nrows:
#     i = i + 1
#     print(table.row_values(i))
#     wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
#     sheet = wbk.add_sheet('Sheet1')
#     sheet.write(table.row_values(i))
#     wbk.save('C:/Users/Alance/PycharmProjects/Python/data.xlsx')

# csvfile = open('C:/Users/Alance/PycharmProjects/Python/data1.csv', 'rb')
# reader = csv.reader(csvfile)
# i = 0
# for line in reader:
#     if i == 0:
#         print(line)
#         i = i + 1
#     csvfile.close()
#
# df = pd.read_csv('C:/Users/Alance/PycharmProjects/Python/data.csv',sep=",")
# print(df.head(10))
# print(df.describe())
# df.columns = ['手机号码', '客户号', '快捷绑卡']
# for i in range(26):
#     df[i*200000:i*200000+199999].to_csv('C:/Users/Alance/PycharmProjects/Python/data%d.csv' %i)
