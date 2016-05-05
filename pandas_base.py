# Coding by SunChuan in 2016/04/26
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import pandas.io.sql as sql
import re

# s = Series([1,2,3,4,5],index=['a','b','c','d','e'])
# print(s)
# print(s.values)
# print(s.index)
# print(s[['a','e']])
#
# pd1 = pd.DataFrame(np.random.randn(5,5),columns = ['year','state','pop','debt','haha'],index = ['one','two','three','four','five'])
#
# print(pd1.year)
# pd1.state = np.arange(5)
# print(pd1)

# df = pd.read_table('D:/1.csv',sep=',')
# print(df.head(10))
# df.to_csv('D:/2.csv',index = False, header = False)
# xls = pd.ExcelFile('D:/2.xlsx')
# table = xls.parse('Sheet1')#读入excel内容
# table.ffill()
# print(table)
# sql.read_frame('select * from ABSOLUTE ')#使用sql读取数据
# pd.merge(df1,df2,how='inner',left_on='',right_on='')
# df.drop_duplicates()

################正则表达式的使用###################
text = "dssa dfa  dafads              gasdf"
print(re.split(r'\s+',text))


#########另外一种写法#################如果对多个字符串使用同样一个一条正则表达式，强烈推荐此种写法
regex = re.compile(r'\s+',flags=re.IGNORECASE)# re.IGNORECASE#############正则表达式不区分大小写
print(regex.split(text))
print(regex.findall(text))#####找到所有匹配的字符串
print(text[regex.search(text).start():regex.search(text).end()])#search 用来查找数据的起始位置



#因此我们强烈建议使用Python的r前缀，就不用考虑转义的问题了：


