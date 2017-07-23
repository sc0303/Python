# Write on 2017/03/23 by SunChuan

import re
import pandas as pd
import pandas.io.sql as sql
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

df = pd.read_excel('D:/PycharmProjects/data/correlation_analysis/异常数量.xlsx')

df_tmp = pysqldf(
    'select ele_created_at,                                                                              \
       sum(case                                                                                     \
             when scename = "商户未接单系统取消" then                                               \
              cnt                                                                                   \
           end) as "商户未接单系统取消",                                                            \
       sum(case                                                                                     \
             when scename = "商户确认前用户取消" then                                               \
              cnt                                                                                   \
           end) as "商户确认前用户取消",                                                            \
       sum(case                                                                                     \
             when scename = "商户确认前商户拒单" then                                               \
              cnt                                                                                   \
           end) as "商户确认前商户拒单",                                                            \
       sum(case                                                                                     \
             when scename = "运力接单前用户取消" then                                               \
              cnt                                                                                   \
           end) as "运力接单前用户取消",                                                            \
       sum(case                                                                                     \
             when scename = "商户确认前风控取消" then                                               \
              cnt                                                                                   \
           end) as "商户确认前风控取消",                                                            \
       sum(case                                                                                     \
             when scename = "运力取餐前用户取消" then                                               \
              cnt                                                                                   \
           end) as "运力取餐前用户取消",                                                            \
       sum(case                                                                                     \
             when scename = "运力接单前商户取消" then                                               \
              cnt                                                                                   \
           end) as "运力接单前商户取消",                                                            \
       sum(case                                                                                     \
             when scename = "运力取餐前商户取消订单" then                                           \
              cnt                                                                                   \
           end) as "运力取餐前商户取消订单",                                                        \
       avg(cnt_total) as "订单数",                                                                  \
       avg(cnt_fail_total) as "异常订单"                                                            \
  from df                                                                                           \
 where scename <> "null"                                                                            \
 group by ele_created_at')
# and ele_created_at>= "2017-02-27"
print(df_tmp.head(10))

# print(df_tmp.corr())
df_tmp.corr(method='pearson').to_excel('D:/PycharmProjects/data/correlation_analysis/result.xlsx', index=True, header=True,
                       sheet_name='result')
