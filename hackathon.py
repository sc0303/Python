# write by Chuan.Sun on 2016/10/16
# python env 3.5.1
__author__ = 'Chuan.Sun'

import pandas as pd
import numpy as np
import math
import scipy
import time
from datetime import datetime


# read the import data
def data_read(read_path):
    try:
        df_order = pd.read_csv('%s/order.csv' % read_path, sep=',',
                               names=['order_id', 'rst_id', 'customer_lng', 'customer_lat', 'maker_order_time',
                                      'promised_at', 'created_at'])
    except:
        print('Wrong order location')
    try:
        df_restaurant = pd.read_csv('%s/restaurant.csv' % read_path, sep=',', names=['rst_id', 'lng', 'lat'])
    except:
        print('Wrong restaurant location')
    return df_order, df_restaurant


# write the data to the specific location
def data_write(write_path, df):
    df.to_csv('%s/result_test.csv' % write_path, 'wb')
    # csvfile = open('C:/Users/Alance/PycharmProjects/Python/2.csv','wb')
    writer = csv.writer(csvfile)


# transform the standard time to timestamp
def time_tansform(standard_time):
    time = datetime.strptime(standard_time, '%Y-%m-%d %H:%M:%S')
    return time.timestamp()
    # print(int(time.timestamp()))


# update the matrix of the rider
def update_rider_data():
    # time_dict_order[] =
    # time_dict_order = dict(sorted(time_dict.items(), key=lambda x: x[0]))
    pass


# find the most suitable rider
def find_suitable_rider():
    # time_dict_order[] =
    # time_dict_order = dict(sorted(time_dict.items(), key=lambda x: x[0]))
    pass


# update the order data
def update_order_data():
    # time_dict_order[] =
    # time_dict_order = dict(sorted(time_dict.items(), key=lambda x: x[0]))
    pass


# calculate the shortest route
def route_calc():
    # 考虑到最初没有骑手的情况
    pass


def calc_distance(lngx, latx, lngy, laty):
    dlat = (latx - laty) / 2
    dlon = (lngx - lngy) / 2
    a = math.sin(dlat * math.pi / 180) ** 2 + math.cos(latx * math.pi / 180) * math.cos(
        laty * math.pi / 180) * math.sin(
            dlon * math.pi / 180) ** 2

    return 2 * math.asin(math.sqrt(a)) * 6378137
    pass


def calc_compensate_money():
    pass


# calculate the cost
def calculate_cost():
    pass




    # dt = datetime(2016, 10, 16, 12, 20) # 用指定日期时间创建datetime
    # dt.timestamp() # 把datetime转换为timestamp
    # dt = dt + datetime.timedelta(hours=-8) # 中国默认时区


#     timestamp = total_seconds(dt - EPOCH)
#     return long(timestamp)

# datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S.%f")
# print('11:11:10')
# return time.strftime("%H:%M:%S",time.localtime(time.time()))








# df = pd.read_table('D:/1.csv',sep=',')
# print(df.head(10))




# csvfile = open('C:/Users/Alance/PycharmProjects/Python/data1.csv', 'rb')
# reader = csv.reader(csvfile)



# with open('C:/Users/Alance/Desktop/需求/报表割接/二维码新脚本.sql', 'r') as f:
#     print(f.read())






if __name__ == '__main__':

    # load the data
    df_order, df_restaurant = data_read('C:/Sample Input')

    # create the matrix of the rider,len(df_order.index) means the number of the order
    rider_matrix = pd.DataFrame(np.zeros((len(df_order.index), 6)),
                                columns=['rider_id', 'rider_realtime_lng', 'rider_realtime_lat', 'redundancy_time',
                                         'status', 'all_order_num'])

    # transform the standard time to timestamp
    df_order.promised_at = df_order.promised_at.apply(lambda x: int(time_tansform(x)))
    df_order.created_at = df_order.created_at.apply(lambda x: int(time_tansform(x)))

    # sort the order data by created_at ascending
    df_order_sort = df_order.sort_values(by='created_at', ascending=True)

    # print(df_order_sort.head(10))
    # print(df_restaurant.head(10))
    # df_order.promised_at = df_order.promised_at.apply(time_tansform,df_order.promised_at)
    # df_order.created_at.apply(time_tansform)

    # create the time point dict,1 means created_at, 2 means promised_at, 3 means the food supply time, 4 means rider arrive the restaurant, 5 means rider arrive the user
    time_dict = {}
    for x in df_order_sort.created_at:
        time_dict[x] = 1

    for x in df_order_sort.promised_at:
        time_dict[x] = 2
    time_dict_order = dict(sorted(time_dict.items(), key=lambda x: x[0]))

    # time_list = list(df_order_sort.created_at)
    # time_list.extend(list(df_order_sort.promised_at))
    # time_list_sorted = sorted(time_list)


    for x, y in time_dict_order.items():
        # if create time
        if y == 1:
            find_suitable_rider()
            update_order_data()
            update_rider_data()
            # del time_dict_order[x]
        elif y == 2:
            update_order_data()
            update_rider_data()
            # del time_dict_order[x]
        elif y == 4:
            update_order_data()
            update_rider_data()
            # del time_dict_order[x]
        elif y == 5:
            update_order_data()
            update_rider_data()
            # del time_dict_order[x]

    calculate_cost()




    # simulate the event
    # while (len(time_dict_order) > 0):
    #
    #
    #




    # update_rider_data()
    #
    # i = 0




    # while (i <= 4 * 3600):
    #     route_calc()
    #     update_rider_data()
    #     update_order_date()
    #     i = i + 1
    # data_write()
    # calculate_cost()




    # data_write('C:/Sample Output',df)
