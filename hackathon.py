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
                                      'promised_at', 'created_at'],
                               dtype={'order_id': np.int64})
    except:
        print('Wrong order location')
    try:
        df_restaurant = pd.read_csv('%s/restaurant.csv' % read_path, sep=',', names=['rst_id', 'lng', 'lat'])
        restaurant_dict = df_restaurant.set_index('rst_id').T.to_dict('list')
    except:
        print('Wrong restaurant location')
    return df_order.head(2), restaurant_dict


# write the data to the specific location
def data_write(write_path, df):
    try:
        df.to_csv('%s/result_test.csv' % write_path, index=False, header=False)
    except:
        print('Wrong output location')


# transform the standard time to timestamp
def time_transform(standard_time):
    separator = str(standard_time)[4:5]
    if separator is '/':
        time = datetime.strptime(standard_time, '%Y/%m/%d %H:%M:%S')
        return time.timestamp()
    elif separator is '-':
        time = datetime.strptime(standard_time, '%Y-%m-%d %H:%M:%S')
        return time.timestamp()
    else:
        print('Wrong input format')


# transform timestamp to the standard time
def time_transform_reverse(timestamp):
    standard_time = datetime.fromtimestamp(timestamp)
    standard_time_formate = time.strftime('%Y/%m/%d %H:%M:%S',
                                          time.strptime(str(standard_time).split(".")[0], '%Y-%m-%d %H:%M:%S'))
    return standard_time_formate


# update the matrix of the rider
def update_rider_free(rider_id):
    rider_matrix.loc[(rider_matrix['rider_id'] == rider_id), 'order_id'] = 0
    rider_matrix.loc[(rider_matrix['rider_id'] == rider_id), 'status'] = 0
    rider_matrix.loc[(rider_matrix['rider_id'] == rider_id), 'all_order_num'] = 0
    rider_matrix.loc[(rider_matrix['rider_id'] == rider_id), 'order_num1'] = 0
    rider_matrix.loc[(rider_matrix['rider_id'] == rider_id), 'order_num2'] = 0

    # rider_matrix[(rider_matrix.rider_id == rider_id)]['order_id'] = 0
    # rider_matrix[(rider_matrix.rider_id == rider_id)]['status'] = 0
    # rider_matrix[(rider_matrix.rider_id == rider_id)]['all_order_num'] = 0
    # rider_matrix[(rider_matrix.rider_id == rider_id)]['order_num1'] = 0
    # rider_matrix[(rider_matrix.rider_id == rider_id)]['order_num2'] = 0

    # time_dict_order[] =
    # time_dict_order = dict(sorted(time_dict.items(), key=lambda x: x[0]))
    pass


# find the most suitable rider
def find_suitable_rider(order_id, rst_id, user_lng, user_lat):
    rst_lng = restaurant_dict[rst_id][0]  # 121
    rst_lat = restaurant_dict[rst_id][1]  # 31
    # the number of the total rider and free rider
    total_rider_num = max(rider_matrix.rider_id)
    free_rider_matrix = rider_matrix[(rider_matrix.status == 0) & (rider_matrix.rider_id != 0)].reset_index(drop=True)
    free_rider_num = len(free_rider_matrix.index)
    # print(rider_matrix)
    # print(free_rider_matrix)
    # not initial status
    if total_rider_num != 0:
        # search for the most suitable rider
        shortest_distance = calc_distance(rst_lng, rst_lat, free_rider_matrix.rider_realtime_lng[0],
                                          free_rider_matrix.rider_realtime_lat[0])
        shortest_distance_to_user = calc_distance(user_lng, user_lat, free_rider_matrix['rider_realtime_lng'][0],
                                                  free_rider_matrix['rider_realtime_lat'][0])
        suitable_rider_id = free_rider_matrix.rider_id[0]

        # the minimum distance to the rst is the minimus distance to deliver
        # print(free_rider_matrix)
        for x in range(1, free_rider_num + 1):
            distance = calc_distance(rst_lng, rst_lat, float(free_rider_matrix['rider_realtime_lng'][x - 1]),
                                     float(free_rider_matrix['rider_realtime_lat'][x - 1]))
            if distance < shortest_distance:
                shortest_distance = distance
                shortest_distance_to_user = calc_distance(user_lng, user_lat,
                                                          free_rider_matrix['rider_realtime_lng'][x - 1],
                                                          free_rider_matrix['rider_realtime_lat'][x - 1])
                suitable_rider_id = free_rider_matrix.rider_id[x - 1]
        promised_at_tmp = int(
                df_order_sort[(df_order_sort['order_id'] == order_id) & (df_order_sort['status'] == 1)]['promised_at'])
        created_at_tmp = int(
                df_order_sort[(df_order_sort['order_id'] == order_id) & (df_order_sort['status'] == 1)]['created_at'])
        maker_order_time_tmp = int(
                df_order_sort[(df_order_sort['order_id'] == order_id) & (df_order_sort['status'] == 1)][
                    'maker_order_time'])
        # rider need waiting to food to make
        if 1.4 * shortest_distance / 3 < maker_order_time_tmp:
            nearest_rider_delivery_time = created_at_tmp + maker_order_time_tmp + 1.4 * shortest_distance_to_user / 3
        else:
            nearest_rider_delivery_time = created_at_tmp + 1.4 * shortest_distance / 3 + 1.4 * shortest_distance_to_user / 3
        # all rider is busy or the nearest rider will not have enough time to accept new order
        # print(1.4 * shortest_distance / 3)
        # print(time_transform_reverse(promised_at_tmp))
        # print(time_transform_reverse(created_at_tmp))
        # print(promised_at_tmp - created_at_tmp)
        # there is no free rider or the nearest rider can not deliver the order in time
        if ((free_rider_num == 0) or (promised_at_tmp < nearest_rider_delivery_time)):
            # call a new rider, set the status to busy and fill the order_id
            rider_matrix.rider_id[total_rider_num] = total_rider_num + 1
            rider_matrix.status[total_rider_num] = 1
            rider_matrix.order_num1[total_rider_num] = order_id
            rider_matrix.order_id[total_rider_num] = order_id
            rider_matrix.rider_realtime_lng[total_rider_num] = user_lng
            rider_matrix.rider_realtime_lat[total_rider_num] = user_lat
            return total_rider_num + 1, rst_lng, rst_lat
        else:  # shortest_distance = calc_distance(rst_lng, rst_lat, free_rider_matrix.rider_realtime_lng[0],
            #                                   free_rider_matrix.rider_realtime_lat[0])
            # suitable_rider_id = free_rider_matrix.rider_id[0]
            # for x in range(1, free_rider_num):
            #     distance = calc_distance(rst_lng, rst_lat, free_rider_matrix.rider_realtime_lng[x],
            #                              free_rider_matrix.rider_realtime_lat[x])
            #     if distance < shortest_distance:
            #         shortest_distance = distance
            #         suitable_rider_id = free_rider_matrix.rider_id[x]
            # set the status to busy and fill the order_id

            # search for the most suitable rider
            rider_matrix.loc[(rider_matrix['rider_id'] == suitable_rider_id), 'status'] = 1
            rider_matrix.loc[(rider_matrix['rider_id'] == suitable_rider_id), 'order_num1'] = order_id
            rider_matrix.loc[(rider_matrix['rider_id'] == suitable_rider_id), 'order_id'] = order_id
            # rider_matrix[(rider_matrix.rider_id == suitable_rider_id)]['status'] = 1
            # rider_matrix[(rider_matrix.rider_id == suitable_rider_id)]['order_num1'] = order_id
            # rider_matrix.status[suitable_rider_id] = 1
            # rider_matrix.order_num1[suitable_rider_id] = order_id
            # print(rider_matrix)

            # print(rider_matrix.rider_realtime_lng[suitable_rider_id])
            # print(rider_matrix.rider_realtime_lat[suitable_rider_id])
            # print(float(rider_matrix[(rider_matrix.rider_id == suitable_rider_id)]['rider_realtime_lng']))
            # print(float(rider_matrix[(rider_matrix.rider_id == suitable_rider_id)]['rider_realtime_lat']))
            # rider_matrix[(rider_matrix.rider_id == suitable_rider_id)]['rider_realtime_lng']
            # rider_matrix[(rider_matrix.rider_id == suitable_rider_id)]['rider_realtime_lat']


            return suitable_rider_id, float(
                    rider_matrix[(rider_matrix.rider_id == suitable_rider_id)]['rider_realtime_lng']), \
                   float(rider_matrix[(rider_matrix.rider_id == suitable_rider_id)]['rider_realtime_lat'])

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
        # return rider_id  # update the order data


def update_sample_output_data(rider_id, order_id, rider_lng, rider_lat, rst_lng, rst_lat, usr_lng,
                              usr_lat, maker_order_time, created_at):
    time_to_arrive_rst = 1.4 * calc_distance(rider_lng, rider_lat, rst_lng, rst_lat) / 3
    take_order_time = max(time_to_arrive_rst, maker_order_time) + created_at
    time_to_arrive_user = take_order_time + 1.4 * calc_distance(
            usr_lng, usr_lat, rst_lng,
            rst_lat) / 3
    # print(time_transform_reverse(take_order_time))
    sample_output_data[(sample_output_data.order_id == order_id) & (sample_output_data.process_id == 1)] = [rider_id,
                                                                                                            1,
                                                                                                            rst_lng,
                                                                                                            rst_lat,
                                                                                                            order_id,
                                                                                                            'take',
                                                                                                            take_order_time]
    sample_output_data[(sample_output_data.order_id == order_id) & (sample_output_data.process_id == 2)] = [rider_id, 2,
                                                                                                            usr_lng,
                                                                                                            usr_lat,
                                                                                                            order_id,
                                                                                                            'delivery',
                                                                                                            time_to_arrive_user]
    # update the time_event
    # loc[row_indexer,col_indexer]
    df_order_sort.loc[
        ((df_order_sort['order_id'] == order_id) & (df_order_sort['status'] == 5)), 'time_point'] = take_order_time
    df_order_sort.loc[(df_order_sort['order_id'] == order_id), 'actual_arrive_at'] = time_to_arrive_user
    # df_order_sort[df_order_sort.order_id == order_id].loc['time_point'] = take_order_time
    # df_order_sort[df_order_sort.order_id == order_id].loc['actual_arrive_at'] = time_to_arrive_user
    # df_order_sort[df_order_sort.order_id == order_id]['time_point'] = take_order_time
    # df_order_sort[df_order_sort.order_id == order_id]['actual_arrive_at'] = time_to_arrive_user
    # take order
    # if process_type == 1:

    # columns=['rider_id', 'process_id', 'rider_realtime_lng', 'rider_realtime_lat',
    #                                     'order_id',
    #                                     'process_type', 'process_time'])
    # deliver order
    # else:
    #     time_to_arrive_user = 1.4 * calc_distance(usr_lng, usr_lat, rst_lng, rst_lng) / 3 + \
    #                           sample_output_data.loc[2 * order_id][6]
    #     sample_output_data.loc[2 * order_id + 1] = {rider_id, 2, usr_lng, usr_lat, order_id, 'delivery',
    #                                                 time_to_arrive_user}
    #     # update the time_event
    #     df_order_sort['time_point'][0] = take_order_time
    #     df_order_sort['actual_arrive_at'][0] = take_order_time + 1.4 * calc_distance(usr_lng, usr_lat, rst_lng,
    #                                                                                  rst_lng) / 3

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
    # sample_output_data['order_id'] = sample_output_data['order_id'].astype('int64')
    # print(df_order_new.head(10))
    print(sample_output_data[sample_output_data.process_id == 2])
    print(df_order_new[df_order_new.status == 1])

    # print(sample_output_data['order_id'].dtype)
    # print(df_order_new['order_id'].dtype)


    df_cost = sample_output_data[sample_output_data.process_id == 2].merge(
            df_order_new[df_order_new.status == 1],
            left_on='order_id', right_on='order_id',
            how='inner')
    print(df_cost.head(10))
    print(df_cost['process_id', 'promised_at'])

    # print(df_cost['process_id', 'promised_at'].apply(lambda x, y: int(calc_compensate_money(x, y))))
    return df_cost['process_id', 'promised_at'].apply(lambda x, y: int(calc_compensate_money(x, y))).sum()
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
    rider_matrix = pd.DataFrame(np.zeros((len(df_order.index), 8), dtype='int64'),
                                columns=['rider_id', 'rider_realtime_lng', 'rider_realtime_lat', 'redundancy_time',
                                         'status', 'all_order_num', 'order_num1', 'order_num2'])

    # create sample out data
    sample_output_data_tmp1 = pd.DataFrame(np.zeros((len(df_order.index), 7),dtype='int64'),
                                           columns=['rider_id', 'process_id', 'rider_realtime_lng',
                                                    'rider_realtime_lat', 'order_id', 'process_type',
                                                    'process_time'])
    sample_output_data_tmp2 = sample_output_data_tmp1.copy(deep=True)
    # as each order have two order action,process_id = 1 means take, process_id = 2 means delivery
    sample_output_data_tmp1['order_id'] = df_order['order_id']
    sample_output_data_tmp1['process_id'] = 1
    sample_output_data_tmp2['order_id'] = df_order['order_id']
    sample_output_data_tmp2['process_id'] = 2
    sample_output_data = sample_output_data_tmp1.append(sample_output_data_tmp2).reset_index(drop=True)

    # transform the standard time to timestamp
    df_order.promised_at = df_order.promised_at.apply(lambda x: int(time_transform(x)))
    df_order.created_at = df_order.created_at.apply(lambda x: int(time_transform(x)))

    df_order_tmp = df_order.copy(deep=True)
    # append the order status column, 1 means created_at, 2 means promised_at, 3 means the food supply time, 4 means rider arrive the restaurant, 5 means rider arrive the user
    df_order['status'] = 1
    df_order_tmp['status'] = 5
    df_order['time_point'] = df_order['created_at']
    df_order_tmp['time_point'] = max(df_order['created_at']) + 1  # to ensure status = 5 stay at the end of the event
    # append the arrive event
    df_order_new = df_order.append(df_order_tmp).reset_index(drop=True)
    # append the actual arrive time of the order
    df_order_new['actual_arrive_at'] = 0

    # sort the order data by created_at ascending
    df_order_sort = df_order_new.sort_values(by='time_point', ascending=True)

    # print(df_order_sort[df_order_sort['status'] == 1])

    i = 0
    while len(df_order_sort.index) > 0:
        order_status = df_order_sort.iloc[0][7]
        order_id = int(df_order_sort.iloc[0][0])
        rst_id = df_order_sort.iloc[0][1]
        user_lng = df_order_sort.iloc[0][2]
        user_lat = df_order_sort.iloc[0][3]
        maker_order_time = df_order_sort.iloc[0][4]
        created_at = df_order_sort.iloc[0][6]
        # if create time

        if order_status == 1:
            # print(df_order_sort)
            suitable_rider_id, rider_lng, rider_lat = find_suitable_rider(order_id, rst_id, user_lng, user_lat)
            update_sample_output_data(suitable_rider_id, order_id, rider_lng, rider_lat, restaurant_dict[rst_id][0],
                                      restaurant_dict[rst_id][1], user_lng,
                                      user_lat, maker_order_time, created_at)
            df_order_sort = df_order_sort.sort_values(by='time_point', ascending=True)
            # print(len(df_order_sort.index))
            df_order_sort.drop(df_order_sort.head(1).index, inplace=True)
            # print('order_status1_sucess')
            # print(df_order_sort)
            continue
        elif order_status == 5:
            # 不需要update_sample_output_data
            # 'rider_id', 'rider_realtime_lng', 'rider_realtime_lat', 'redundancy_time',
            # 'status', 'all_order_num', 'order_num1', 'order_num2'
            # print(rider_matrix)
            # if i ==7:
            #     print('test')
            #     print(rider_matrix)
            #     print(order_id)
            #     print(rider_matrix.loc[(rider_matrix['order_num1'] == order_id), 'rider_id'])
            update_rider_free(int(rider_matrix.loc[(rider_matrix['order_num1'] == order_id), 'rider_id']))
            df_order_sort = df_order_sort.sort_values(by='time_point', ascending=True)
            df_order_sort.drop(df_order_sort.head(1).index, inplace=True)
            # print('order_status5_sucess')
            # print(df_order_sort)
            i = i + 1
            continue

# write the output file to the specific location

# print(time_transform_reverse(time_transform('2016-12-10 21:37:15')))

# df['data1'].groupby([df['key1'], df['key2']]).mean()
rider_total_order_num = dict(sample_output_data.groupby(['rider_id']).size())
# sample_output_data_sort = sample_output_data.sort_values(by=['rider_id', 'process_time'], ascending=False).reset_index(
#     drop=True)

df_finally = pd.DataFrame(columns=['rider_id', 'process_id', 'rider_realtime_lng',
                                   'rider_realtime_lat', 'order_id', 'process_type',
                                   'process_time'], dtype='int64')
for x in rider_total_order_num:
    df_tmp = sample_output_data[sample_output_data.rider_id == x]
    df_tmp = df_tmp.sort_values(by=['rider_id', 'process_time'], ascending=True).reset_index(
            drop=True)
    for y in range(0, len(df_tmp.index)):
        df_tmp.loc[y, 'process_id'] = y + 1
        # df_tmp['process_id'][y] = y + 1
    df_finally = df_finally.append(df_tmp)

# print(df_finally)

# for x in range(0, len(sample_output_data_sort.index)):
#     dict[int(rider_total_order_num['rider_id'][x])]
#     sample_output_data_sort['rider_id'][x] = dict[int(sample_output_data_sort['rider_id'][x])]

df_finally.process_time = df_finally.process_time.apply(lambda x: time_transform_reverse(x))
df_finally = df_finally.sort_values(by=['rider_id', 'process_time'], ascending=True).reset_index(
        drop=True)
# print(sample_output_data_sort)
data_write('C:/Sample Output', df_finally)

calculate_cost()

A.merge(B, left_on='lkey', right_on='rkey', how='outer')

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




# elif order_status == 2:
#         update_order_data()
#         update_rider_data()
#         # del the first event and the other will move forward and resort the time event
#         event_time_list_order = event_time_list_order.sort(key=lambda x: x[0])
#         event_time_list_order.remove(0)
#         # if supply food time
#     elif order_status == 3:
#         update_order_data()
#         update_rider_data()
#         # del the first event and the other will move forward and resort the time event
#         event_time_list_order = event_time_list_order.sort(key=lambda x: x[0])
#         event_time_list_order.remove(0)
#         # if arrive the restaurant time
#     elif order_status == 4:
#         update_order_data()
#         update_rider_data()
#         # del the first event and the other will move forward and resort the time event
#         event_time_list_order = event_time_list_order.sort(key=lambda x: x[0])
#         event_time_list_order.remove(0)
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


# # append the time point of the event
# df_order_new['time_point'] = 0
#
# print(df_order_new[['created_at', 'status']].head(10))
# # print(df_order_new[['created_at', 'status']].apply(lambda x, y: x if y == 1 else 0))
# df_order_new.time_point = df_order_new[['created_at', 'status']].apply(lambda x, y: x if y == 1 else 0)
# print(df_order_new.head(10))


# update_order_data()
# update_rider_data()
# # del the first event and the other will move forward and resort the time event
# event_time_list_order = event_time_list_order.sort(key=lambda x: x[0])
# event_time_list_order.remove(0)

# update_rider_data()
# del the first event and the other will move forward and resort the time event
# event_time_list_order = event_time_list_order.sort(key=lambda x: x[0])
# event_time_list_order.remove(0)
# if promised arrive time

# if actually arrive time
# rider_matrix.loc[0] = {'rider_id': 1}
# rider_matrix.iloc[0][0] = 100
# print(rider_matrix)

# data.drop(n)可以删除第i行
# import pandas as pd
# data=pd.DataFrame([[1,2,3],[4,5,6]])
# print data.drop(0)
