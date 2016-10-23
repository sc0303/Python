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
        restaurant_dict = df_restaurant.set_index('rst_id').T.to_dict('list')
    except:
        print('Wrong restaurant location')
    return df_order, restaurant_dict


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
def find_suitable_rider(order_id, user_lng, user_lat):
    print(rider_matrix)
    print(len(rider_matrix[rider_matrix.status == 0].index))
    print('hello')
    rst_lng = restaurant_dict[order_id][0]  # 121
    rst_lat = restaurant_dict[order_id][1]  # 31
    # the number of the total rider and free rider
    total_rider_num = max(rider_matrix.rider_id)
    free_rider_matrix = rider_matrix[(rider_matrix.status == 0) & (rider_matrix.rider_id != 0)]
    free_rider_num = len(free_rider_matrix.index)
    # not initial status
    if total_rider_num != 0:
        # all rider is busy
        if free_rider_num == 0:
            # call a new rider, set the status to busy and fill the order_id
            rider_matrix.rider_id[total_rider_num] = total_rider_num + 1
            rider_matrix.status[total_rider_num] = 1
            rider_matrix.order_num1[total_rider_num] = order_id
            rider_matrix.rider_realtime_lng[total_rider_num] = rst_lng
            rider_matrix.rider_realtime_lat[total_rider_num] = rst_lat
            return total_rider_num + 1, rst_lng, rst_lat
        else:
            # search for the most suitable rider
            shortest_distance = calc_distance(rst_lng, rst_lat, free_rider_matrix.rider_realtime_lng[0],
                                              free_rider_matrix.rider_realtime_lat[0])
            for x in range(1, free_rider_num):
                distance = calc_distance(rst_lng, rst_lat, free_rider_matrix.rider_realtime_lng[x],
                                         free_rider_matrix.rider_realtime_lat[x])
                if distance < shortest_distance:
                    shortest_distance = distance
                    suitable_rider_id = free_rider_matrix.rider_id[x]
            # set the status to busy and fill the order_id
            rider_matrix.status[suitable_rider_num] = 1
            rider_matrix.order_num1[suitable_rider_num] = order_id
            # rider_matrix.rider_realtime_lng[suitable_rider_num] = rst_lng
            # rider_matrix.rider_realtime_lat[suitable_rider_num] = rst_lat
            return suitable_rider_id, rider_matrix.rider_realtime_lng[suitable_rider_num],
            rider_matrix.rider_realtime_lat[suitable_rider_num]

    # the initial status
    else:  # add a new rider, set the status to busy and fill the order_id,rider location
        rider_matrix.rider_id[0] = 1
    rider_matrix.status[0] = 1
    rider_matrix.order_num1[0] = order_id
    rider_matrix.rider_realtime_lng[0] = rst_lng
    rider_matrix.rider_realtime_lat[0] = rst_lat
    return 1, rst_lng, rst_lat  # return
    # print(max(rider_matrix.rider_id))
    # time_dict_order[] =
    # time_dict_order = dict(sorted(time_dict.items(), key=lambda x: x[0]))
    # return rider_id


# update the order data
def update_sample_output_data(rider_id, process_type, order_id, rider_lng, rider_lat, rst_lng, rst_lat, usr_lng,
                              usr_lat, maker_order_time, created_at):
    # take order
    if process_type == 1:
        time_to_arrive_rst = 1.4 * calc_distance(rider_lng, rider_lat, rst_lng, rst_lng) / 3 +max(time_to_arrive_rst, maker_order_time)
        sample_output_data.loc[2 * order_id] = {rider_id, 1, rst_lng, rst_lat, order_id, 'take', time_to_arrive_rst}
        # columns=['rider_id', 'process_id', 'rider_realtime_lng', 'rider_realtime_lat',
        #                                     'order_id',
        #                                     'process_type', 'process_time'])
        pass
    # deliver order
    else:
        time_to_arrive_user = 1.4 * calc_distance(usr_lng, usr_lat, rst_lng, rst_lng) / 3 + \
                              sample_output_data.loc[2 * order_id][6]
        sample_output_data.loc[2 * order_id + 1] = {rider_id, 2, usr_lng, usr_lat, order_id, 'delivery', time_to_arrive_user}
        pass

    # time_dict_order[] =
    # time_dict_order = dict(sorted(time_dict.items(), key=lambda x: x[0]))
    # process_time =

    # sample_out_data  # calculate the shortest route


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


def calc_compensate_money(t, promised_at):
    a = (t - promised_at) / 60
    if a < 0:
        return 0
    else:
        return (math.ceil(math.log(a + 1) * a + 5))


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
    df_order, restaurant_dict = data_read('C:/Sample Input')

    # create the matrix of the rider,len(df_order.index) means the number of the order status = 1 means is busy, status = 0 means free
    # rider_matrix = pd.DataFrame(columns=['rider_id', 'rider_realtime_lng', 'rider_realtime_lat', 'redundancy_time',
    #                                      'status', 'all_order_num', 'order_num1', 'order_num2'])
    rider_matrix = pd.DataFrame(np.zeros((len(df_order.index), 8)),
                                columns=['rider_id', 'rider_realtime_lng', 'rider_realtime_lat', 'redundancy_time',
                                         'status', 'all_order_num', 'order_num1', 'order_num2'])

    # sample out data
    sample_output_data = pd.DataFrame(np.zeros((len(df_order.index) * 2, 8)),
                                      columns=['rider_id', 'process_id', 'rider_realtime_lng', 'rider_realtime_lat',
                                               'order_id',
                                               'process_type', 'process_time'])

    # rider_matrix.loc[0] = {'rider_id': 1}
    # rider_matrix.iloc[0][0] = 100
    # print(rider_matrix)

    # data.drop(n)可以删除第i行
    # import pandas as pd
    # data=pd.DataFrame([[1,2,3],[4,5,6]])
    # print data.drop(0)




    # transform the standard time to timestamp
    df_order.promised_at = df_order.promised_at.apply(lambda x: int(time_tansform(x)))
    df_order.created_at = df_order.created_at.apply(lambda x: int(time_tansform(x)))

    # append the order status column, 1 means created_at, 2 means promised_at, 3 means the food supply time, 4 means rider arrive the restaurant, 5 means rider arrive the user
    df_order['status'] = 1

    # sort the order data by created_at ascending
    df_order_sort = df_order.sort_values(by='created_at', ascending=True)
    # print(df_order_sort.head(10))
    # print(df_restaurant.head(10))
    # df_order.promised_at = df_order.promised_at.apply(time_tansform,df_order.promised_at)
    # df_order.created_at.apply(time_tansform)

    # create the time point list,the first element means the create_at,the second element means the order order_id, and the third element means status as:
    # 1 means created_at, 2 means promised_at, 3 means the food supply time, 4 means rider arrive the restaurant, 5 means rider arrive the user
    # event_time_list = [[0, 0, 0]] * len(df_order.index) * 5
    # for x in range(0, len(df_order.index) * 5, 5):
    #     event_time_list[x] = [df_order_sort.created_at[x / 5], df_order_sort.order_id[x / 5], 1]
    #     event_time_list[x + 1] = [df_order_sort.promised_at[x / 5], df_order_sort.order_id[x / 5], 2]
    #     event_time_list[x + 2] = [df_order_sort.maker_order_time[x / 5], df_order_sort.order_id[x / 5], 3]
    # print(event_time_list)

    # sort the event_time_list by time
    # event_time_list_order = event_time_list.sort(key=lambda x: x[0])
    # print(event_time_list_order)
    # event_time_list_order = list(sorted(event_time_list.items(), key=lambda x: x[0]))

    # for x in df_order_sort.created_at:
    #     time_dict[x] = 1
    #
    # for x in df_order_sort.promised_at:
    #     time_dict[x] = 2
    # time_dict_order = dict(sorted(time_dict.items(), key=lambda x: x[0]))

    # time_list = list(df_order_sort.created_at)
    # time_list.extend(list(df_order_sort.promised_at))
    # time_list_sorted = sorted(time_list)

    while len(df_order_sort.index) > 0:
        order_status = df_order_sort.iloc[0][7]
        order_id = df_order_sort.iloc[0][0]
        user_lng = df_order_sort.iloc[0][2]
        user_lat = df_order_sort.iloc[0][3]
        # if create time
        if order_status == 1:
            suitable_rider_id, rider_lng, rider_lat = find_suitable_rider(order_id, user_lng, user_lat)
            update_sample_output_data()
            update_rider_data()
            # del the first event and the other will move forward and resort the time event
            event_time_list_order = event_time_list_order.sort(key=lambda x: x[0])
            event_time_list_order.remove(0)
            # if promised arrive time
        elif order_status == 2:
            update_order_data()
            update_rider_data()
            # del the first event and the other will move forward and resort the time event
            event_time_list_order = event_time_list_order.sort(key=lambda x: x[0])
            event_time_list_order.remove(0)
            # if supply food time
        elif order_status == 3:
            update_order_data()
            update_rider_data()
            # del the first event and the other will move forward and resort the time event
            event_time_list_order = event_time_list_order.sort(key=lambda x: x[0])
            event_time_list_order.remove(0)
            # if arrive the restaurant time
        elif order_status == 4:
            update_order_data()
            update_rider_data()
            # del the first event and the other will move forward and resort the time event
            event_time_list_order = event_time_list_order.sort(key=lambda x: x[0])
            event_time_list_order.remove(0)
            # if actually arrive time
        elif order_status == 5:
            update_order_data()
            update_rider_data()
            # del the first event and the other will move forward and resort the time event
            event_time_list_order = event_time_list_order.sort(key=lambda x: x[0])
            event_time_list_order.remove(0)

    calculate_cost()

    print(calc_compensate_money(300, 0))


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
