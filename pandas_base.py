# Coding by SunChuan in 2016/04/26
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import pandas.io.sql as sql

# s = Series([1,2,3,4,5],index=['a','b','c','d','e'])
# print(s)
# print(s.values)
# print(s.index)
# print(s[['a','e']])
<<<<<<< HEAD

# pd1 = pd.DataFrame(np.random.randn(5,5),columns = ['year','state','pop','debt','haha'],index = ['one','two','three','four','five'])

# print(pd1)
# pd1.state = np.arange(5)
# print(pd1)
# pd1.columns.name = 'states'
# print(pd1.columns.name)
# states = ['year','state','pop','debt','haha']
# pd2 = pd1.reindex(index = ['a','b','c','d','e'],method = 'ffill',columns=states)
# print(pd2)
# print(pd1.drop('year',axis=2, errors='ignore'))
# df = DataFrame(np.random.randn(3, 3), columns=['A', 'B', 'C'])
# print(df)
# print(df.drop('A', axis=1, errors='ignore'))

df1 = pd.DataFrame(np.arange(9).reshape(3,3),columns= list('abc'),index=['1','2','3'])
df2 = pd.DataFrame(np.arange(12).reshape(3,4),columns= list('abde'))
print(df1)
print(df2)
print(df1+df2)
print(df1.add(df2,fill_value = 0))
=======
#
# pd1 = pd.DataFrame(np.random.randn(5,5),columns = ['year','state','pop','debt','haha'],index = ['one','two','three','four','five'])
#
# print(pd1.year)
# pd1.state = np.arange(5)
# print(pd1)
<<<<<<< HEAD
>>>>>>> dev
=======

# df = pd.read_table('D:/1.csv',sep=',')
# print(df.head(10))
# df.to_csv('D:/2.csv',index = False, header = False)
xls = pd.ExcelFile('D:/2.xlsx')
table = xls.parse('Sheet1')#读入excel内容
table.ffill()
print(table)
sql.read_frame('select * from ABSOLUTE ')#使用sql读取数据
pd.merge(df1,df2,how='inner',left_on='',right_on='')
df.drop_duplicates()
>>>>>>> dev
