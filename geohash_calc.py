# write on 2017/07/03 by chuan.sun
import geohash
import pandas as pd

# import python-geohash
# from geohash import encode,decode,adjacent, neighbors, neighborsfit
# geohash.neighbors("abx1")

df_geohash = pd.read_excel('C:/2017-07-03-geohash.xlsx')
df_geohash['neighbors'] = 0

# print(df_geohash.head(10))

j = 0
for i in df_geohash.iloc[:, 0]:
    df_geohash.iloc[j, 1] = str(geohash.neighbors(i[0:5]))
    j = j + 1

df_geohash.to_csv('D:/1.csv')
