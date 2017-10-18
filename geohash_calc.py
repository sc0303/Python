# write on 2017/07/03 by chuan.sun
import itertools

import geohash
import pandas as pd

# import python-geohash
# from geohash import encode,decode,adjacent, neighbors, neighborsfit
# geohash.neighbors("abx1")

df_geohash = pd.read_excel('D:/kfc.xlsx')
df_geohash['neighbors'] = 0
j = 0
for i in df_geohash.iloc[:, 2]:
    # list_temp.append(geohash.neighbors(i))
    df_geohash.iloc[j, 3] = str(geohash.neighbors(i))
    j = j + 1

# print(df_geohash.head(10))
#
# a = [1, 2, 2, 2, 2]
# b = tuple(a)
# print(b)
#
# j = 0
# for i in df_geohash.iloc[:, 0]:
#     nine_list = geohash.neighbors(i[0:5])
#     list_temp = list()
#     for x in nine_list:
#         list_temp.append(geohash.neighbors(x))
#     list_temp = list(itertools.chain.from_iterable(list_temp))
#     list_temp = [x[:4] for x in list_temp]
#     # print(list_temp)
#     list_set = set(list_temp)
#     # print(list_set)
#     list_temp = list(list_set)
#     if len(list_temp) ==2:
#         list_temp.append('testtest')
#         list_temp.append('testtest')
#     df_geohash.iloc[j, 1] = str(list_temp)
#     j = j + 1
#
df_geohash.to_csv('D:/1.csv')
