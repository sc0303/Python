import pandas as pd
import numpy as np
import time
import os
import xlrd

# #######################################calculate the distinct user#######################
print('Please insure your file is under directory D:\data and your file type should be .xlsx\n')
time.sleep(1)
input("Press enter if your are already")
df_result = pd.DataFrame(columns=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19'])
try:
    for f in os.listdir('D:\\data'):
        print("Reading file:",f)
        df_tmp = pd.read_excel('D:\\data\\%s' %f,index_col = None, header = 0)
        df_tmp.columns = (['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19'])
        df = df_tmp[2:]
        # df.head(10).to_excel('D:\\data\\data1.xlsx')
        # df_result.head(10).to_excel('D:\\data\\data2.xlsx')
        df_result = pd.concat([df_result,df])
    df_groupby = df_result.groupby(['1','2','3','4','5'])['12'].nunique()
    # pd_finally = pd.DataFrame(df_groupby,columns=['商户省份','商户地市','企业账号','商户编码','商户名称','交易笔数'])
    pd_finally = pd.DataFrame(df_groupby)
    # pd_finally.columns = (['商户省份','商户地市','企业账号','商户编码','商户名称','交易笔数'])
    # print(pd_finally.describe())
    # print(pd_finally.head(10))
    pd_finally.to_excel('D:\\data\\suzi.xlsx')
    print('Job done! You can find the result in suzi.xlsx')
    time.sleep(10)

except IOError:
    print("Can't find the location of th file")







    # df_groupby = df_result.groupby(['1']).count()
    # print(df_groupby.head(10))
    # df_groupby.to_excel('D:\\data\\data.xlsx', index=False,header=False)
    # print(df_groupby.head(10))
    #
    #
    #
    #     # print(df_title)
    #     df_result = df_result.append(df_title)
    #     # print(df_title)
    #     df = df_tmp[2:]
    #     df.gro
    #     table.groupby('YEARMONTH').CLIENTCODE.nunique()
    #     # print(df.describe())
    # # print(df.head(10))
    # df_title = df_tmp[1:2]
    # df_result.to_excel('D:\\data\\data.xlsx', index=False,header=False)
# print('Plase insure your file directory is D: and rename your file name as data.csv\n')
# file_type = str(input("Please input the format of your file(support xlsx or cvs only)"))
#
# if file_type == xlsx:
#
# elif file_type == cvs:
#     try:
#         df = pd.read_csv('D:/data.csv', sep=",")
#         print(df.head(10))
#         print('the base info about the file as follows\n')
#         print(df.describe())
#
#         # df.columns = ['手机号码', '客户号', '快捷绑卡']
#         print('%d line data has been loaded' % (df.shape[0]))
#         for i in range(df.shape[0] // line_num + 1):
#             df[i * line_num:i * line_num + line_num - 1].to_csv('D:/data%d.csv' % i, index=False,
#                                                                 header=False)  # index后面可以控制不输出行、列索引
#         print('Job done!')
#         time.sleep(10)
#     except IOError:
#         print('Your file is not in the right location or your file name is wrong')
# else:
#     print("Sorry, the program does not support the format")
# line_num = int(input("Please input the each size of the file:"))
