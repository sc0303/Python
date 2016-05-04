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
#
# pd1 = pd.DataFrame(np.random.randn(5,5),columns = ['year','state','pop','debt','haha'],index = ['one','two','three','four','five'])
#
# print(pd1.year)
# pd1.state = np.arange(5)
# print(pd1)

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