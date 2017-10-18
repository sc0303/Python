# Write on 2017/08/28 by Chuan.Sun
import numpy as np
import pandas as pd
from pandasql import sqldf
from sklearn.preprocessing import MinMaxScaler

pysqldf = lambda q: sqldf(q, globals())

data = pd.read_excel('D:/KA.xlsx')
look_up_table = pd.read_excel('D:/lookup_table.xlsx')

# 选择训练集，即最近90天的历史数据
data_fit = pysqldf("SELECT  * FROM data where dt<='2017-08-28';")

# 将数据按照时间维度进行list化
data_fit_group = data.join(
    data_fit.groupby(['aera_region', 'province_name', 'first_category', 'target'])['valid_cnt'].apply(list).to_frame(
        'target_list'), on=['aera_region', 'province_name', 'first_category', 'target'])
print(data_fit_group.shape)

# 选择预测数据，减少数据计算量,关联lookup_table
data_fit_group_transform = data_fit_group[data_fit_group['dt'] == '2017-08-28'].merge(look_up_table, left_on='target',
                                                                                      right_on='target_code')

print(data_fit_group_transform.shape)

# 计算数据分位点
data_fit_group_transform.loc[:, 'IQR'] = data_fit_group_transform.loc[:, 'target_list'].apply(
    lambda x: np.percentile(x, 75) - np.percentile(x, 25))
data_fit_group_transform.loc[:, 'Q3'] = data_fit_group_transform.loc[:, 'target_list'].apply(
    lambda x: np.percentile(x, 75))
data_fit_group_transform.loc[:, 'Q1'] = data_fit_group_transform.loc[:, 'target_list'].apply(
    lambda x: np.percentile(x, 25))
data_fit_group_transform.loc[:, 'Q3_plus_1_5IQR'] = data_fit_group_transform.loc[:, 'target_list'].apply(
    lambda x: np.percentile(x, 75)) + 1.5 * data_fit_group_transform.loc[:, 'IQR']
data_fit_group_transform.loc[:, 'Q3_plus_3IQR'] = data_fit_group_transform.loc[:, 'target_list'].apply(
    lambda x: np.percentile(x, 75)) + 3 * data_fit_group_transform.loc[:, 'IQR']
data_fit_group_transform.loc[:, 'Q1_minus_1_5IQR'] = data_fit_group_transform.loc[:, 'target_list'].apply(
    lambda x: np.percentile(x, 25)) - 1.5 * data_fit_group_transform.loc[:, 'IQR']
data_fit_group_transform.loc[:, 'Q1_minus_3IQR'] = data_fit_group_transform.loc[:, 'target_list'].apply(
    lambda x: np.percentile(x, 25)) - 3 * data_fit_group_transform.loc[:, 'IQR']

# 加入对IQR为0数据的已处理
data_fit_group_transform_IQR_filter = data_fit_group_transform[data_fit_group_transform['IQR'] > 0]
data_fit_group_transform_IQR = data_fit_group_transform[data_fit_group_transform['IQR'] == 0]

# 异常判断
# 正常
cond1 = (data_fit_group_transform_IQR_filter.loc[:, 'valid_cnt'] <= data_fit_group_transform_IQR_filter.loc[:,
                                                                    'Q3_plus_1_5IQR']) & (
            data_fit_group_transform_IQR_filter.loc[:, 'valid_cnt'] >= data_fit_group_transform_IQR_filter.loc[:,
                                                                       'Q1_minus_1_5IQR'])
# 橙色告警
cond2_1 = ((data_fit_group_transform_IQR_filter.loc[:, 'valid_cnt'] < data_fit_group_transform_IQR_filter.loc[:,
                                                                      'Q1_minus_1_5IQR']) & (
               data_fit_group_transform_IQR_filter.loc[:, 'valid_cnt'] >= data_fit_group_transform_IQR_filter.loc[:,
                                                                          'Q1_minus_3IQR']))
cond2_2 = ((data_fit_group_transform_IQR_filter.loc[:, 'valid_cnt'] > data_fit_group_transform_IQR_filter.loc[:,
                                                                      'Q3_plus_1_5IQR']) & (
               data_fit_group_transform_IQR_filter.loc[:, 'valid_cnt'] <= data_fit_group_transform_IQR_filter.loc[:,
                                                                          'Q3_plus_3IQR']))
cond2 = cond2_1 | cond2_2
# 红色告警
cond3_1 = (
    data_fit_group_transform_IQR_filter.loc[:, 'valid_cnt'] < data_fit_group_transform_IQR_filter.loc[:,
                                                              'Q1_minus_3IQR'])
cond3_2 = (
    data_fit_group_transform_IQR_filter.loc[:, 'valid_cnt'] > data_fit_group_transform_IQR_filter.loc[:,
                                                              'Q3_plus_3IQR'])
cond3 = cond3_1 | cond3_2

# 告警结果
rst2_1 = 10 * data_fit_group_transform_IQR_filter.loc[:, 'target_normalize'] * (
abs(data_fit_group_transform_IQR_filter.loc[:, 'valid_cnt'] - data_fit_group_transform_IQR_filter.loc[:,
                                                              'Q1_minus_1_5IQR']) / data_fit_group_transform_IQR_filter.loc[
                                                                                    :, 'IQR'])
rst2_2 = 10 * data_fit_group_transform_IQR_filter.loc[:, 'target_normalize'] * (
abs(data_fit_group_transform_IQR_filter.loc[:, 'valid_cnt'] - data_fit_group_transform_IQR_filter.loc[:,
                                                              'Q3_plus_1_5IQR']) / data_fit_group_transform_IQR_filter.loc[
                                                                                   :, 'IQR'])

rst3_1 = 20 * data_fit_group_transform_IQR_filter.loc[:, 'target_normalize'] * (
abs(data_fit_group_transform_IQR_filter.loc[:, 'valid_cnt'] - data_fit_group_transform_IQR_filter.loc[:,
                                                              'Q1_minus_3IQR']) / data_fit_group_transform_IQR_filter.loc[
                                                                                  :, 'IQR'])
rst3_2 = 20 * data_fit_group_transform_IQR_filter.loc[:, 'target_normalize'] * (
abs(data_fit_group_transform_IQR_filter.loc[:, 'valid_cnt'] - data_fit_group_transform_IQR_filter.loc[:,
                                                              'Q3_plus_3IQR']) / data_fit_group_transform_IQR_filter.loc[
                                                                                 :, 'IQR'])

# 异常等级计算
data_fit_group_transform_IQR_filter.loc[:, 'abnormal_level'] = np.where(cond1, 0, np.where(cond2_1, rst2_1,
                                                                                           np.where(cond2_2, rst2_2,
                                                                                                    np.where(cond3_1,
                                                                                                             rst3_1,
                                                                                                             rst3_2))))

data_fit_group_transform_IQR_filter.loc[:, 'abnormal_level_name'] = np.where(cond1, '正常', np.where(cond2_1, '异常低',
                                                                                                   np.where(cond2_2,
                                                                                                            '异常高',
                                                                                                            np.where(
                                                                                                                cond3_1,
                                                                                                                '非常低',
                                                                                                                '非常高'))))

# 计算异常值
data_fit_group_transform_IQR_filter.loc[:, 'monitor_result'] = data_fit_group_transform_IQR_filter.loc[
                                                               :, 'abnormal_level']

data_fit_group_transform_IQR_filter.loc[:, 'monitor_result_normalize'] = 0

# 判断是否有对应的异常项，区分不同的异常等级以及指标的正负相关性，分别进行指标归一化
if data_fit_group_transform_IQR_filter[data_fit_group_transform_IQR_filter['abnormal_level_name'] == '正常'].shape[0] > 0:
    data_fit_group_transform_IQR_filter.ix[
        data_fit_group_transform_IQR_filter['abnormal_level_name'] == '正常', 'monitor_result_normalize'] = 80

# 橙色告警——异常低
if data_fit_group_transform_IQR_filter[(
            data_fit_group_transform_IQR_filter['abnormal_level_name'] == '异常低') & (
            data_fit_group_transform_IQR_filter[
                'correlation'] == 1)].shape[
    0] > 0:
    data_fit_group_transform_IQR_filter.ix[(data_fit_group_transform_IQR_filter['abnormal_level_name'] == '异常低') & (
        data_fit_group_transform_IQR_filter['correlation'] == 1), 'monitor_result_normalize'] = MinMaxScaler(
        feature_range=(-0.5, 0.5)).fit_transform(np.array(data_fit_group_transform_IQR_filter.ix[
                                                              (data_fit_group_transform_IQR_filter[
                                                                   'abnormal_level_name'] == '异常低') & (
                                                                  data_fit_group_transform_IQR_filter[
                                                                      'correlation'] == 1), 'monitor_result']).reshape(
        -1, 1)) * 40 + 60
if data_fit_group_transform_IQR_filter[(
            data_fit_group_transform_IQR_filter['abnormal_level_name'] == '异常低') & (
            data_fit_group_transform_IQR_filter['correlation'] == -1)].shape[0] > 0:
    data_fit_group_transform_IQR_filter.ix[
        (data_fit_group_transform_IQR_filter['abnormal_level_name'] == '异常低') & (data_fit_group_transform_IQR_filter[
                                                                                     'correlation'] == -1), 'monitor_result_normalize'] = MinMaxScaler().fit_transform(
        np.array(data_fit_group_transform_IQR_filter.ix[
                     (data_fit_group_transform_IQR_filter['abnormal_level_name'] == '异常低') & (
                         data_fit_group_transform_IQR_filter[
                             'correlation'] == -1), 'monitor_result']).reshape(-1, 1)) * (-10) + 90

# 红色告警——非常低
if data_fit_group_transform_IQR_filter[(
            data_fit_group_transform_IQR_filter['abnormal_level_name'] == '非常低') & (data_fit_group_transform_IQR_filter[
                                                                                        'correlation'] == 1)].shape[
    0] > 0:
    data_fit_group_transform_IQR_filter.ix[
        (data_fit_group_transform_IQR_filter['abnormal_level_name'] == '非常低') & (data_fit_group_transform_IQR_filter[
                                                                                     'correlation'] == 1), 'monitor_result_normalize'] = MinMaxScaler(
        feature_range=(-0.5, 0.5)).fit_transform(np.array(data_fit_group_transform_IQR_filter.ix[(
                                                                                                     data_fit_group_transform_IQR_filter[
                                                                                                         'abnormal_level_name'] == '非常低') & (
                                                                                                     data_fit_group_transform_IQR_filter[
                                                                                                         'correlation'] == 1), 'monitor_result']).reshape(
        -1, 1)
    ) * 40 + 20
if data_fit_group_transform_IQR_filter[(
            data_fit_group_transform_IQR_filter['abnormal_level_name'] == '非常低') & (
            data_fit_group_transform_IQR_filter[
                'correlation'] == -1)].shape[
    0] > 0:
    data_fit_group_transform_IQR_filter.ix[(
                                               data_fit_group_transform_IQR_filter['abnormal_level_name'] == '非常低') & (
                                               data_fit_group_transform_IQR_filter[
                                                   'correlation'] == -1), 'monitor_result_normalize'] = MinMaxScaler().fit_transform(
        np.array(data_fit_group_transform_IQR_filter.ix[(
                                                            data_fit_group_transform_IQR_filter[
                                                                'abnormal_level_name'] == '非常低') & (
                                                            data_fit_group_transform_IQR_filter[
                                                                'correlation'] == -1), 'monitor_result']).reshape(-1, 1)
    ) * (-10) + 100
# 橙色告警——异常高
if data_fit_group_transform_IQR_filter[(data_fit_group_transform_IQR_filter['abnormal_level_name'] == '异常高') & (
            data_fit_group_transform_IQR_filter[
                'correlation'] == 1)].shape[
    0] > 0:
    data_fit_group_transform_IQR_filter.ix[
        (data_fit_group_transform_IQR_filter['abnormal_level_name'] == '异常高') & (data_fit_group_transform_IQR_filter[
                                                                                     'correlation'] == 1), 'monitor_result_normalize'] = MinMaxScaler().fit_transform(
        np.array(data_fit_group_transform_IQR_filter.ix[(
                                                            data_fit_group_transform_IQR_filter[
                                                                'abnormal_level_name'] == '异常高') & (
                                                            data_fit_group_transform_IQR_filter[
                                                                'correlation'] == 1), 'monitor_result']).reshape(-1, 1)
    ) * 10 + 80
if data_fit_group_transform_IQR_filter[(
            data_fit_group_transform_IQR_filter['abnormal_level_name'] == '异常高') & (
            data_fit_group_transform_IQR_filter[
                'correlation'] == -1)].shape[
    0] > 0:
    data_fit_group_transform_IQR_filter.ix[
        (data_fit_group_transform_IQR_filter['abnormal_level_name'] == '异常高') & (data_fit_group_transform_IQR_filter[
                                                                                     'correlation'] == -1), 'monitor_result_normalize'] = MinMaxScaler(
        feature_range=(-0.5, 0.5)).fit_transform(np.array(data_fit_group_transform_IQR_filter.ix[(
                                                                                                     data_fit_group_transform_IQR_filter[
                                                                                                         'abnormal_level_name'] == '异常高') & (
                                                                                                     data_fit_group_transform_IQR_filter[
                                                                                                         'correlation'] == -1), 'monitor_result']).reshape(
        -1, 1)
    ) * (-40) + 60

# 红色告警——非常高
if data_fit_group_transform_IQR_filter[(data_fit_group_transform_IQR_filter['abnormal_level_name'] == '非常高') & (
            data_fit_group_transform_IQR_filter[
                'correlation'] == 1)].shape[
    0] > 0:
    data_fit_group_transform_IQR_filter.ix[(data_fit_group_transform_IQR_filter[
                                                'abnormal_level_name'] == '非常高') & (data_fit_group_transform_IQR_filter[
                                                                                        'correlation'] == 1), 'monitor_result_normalize'] = MinMaxScaler().fit_transform(
        np.array(data_fit_group_transform_IQR_filter.ix[(
                                                            data_fit_group_transform_IQR_filter[
                                                                'abnormal_level_name'] == '非常高') & (
                                                            data_fit_group_transform_IQR_filter[
                                                                'correlation'] == 1), 'monitor_result']).reshape(-1, 1)
    ) * 10 + 90
if data_fit_group_transform_IQR_filter[(
            data_fit_group_transform_IQR_filter['abnormal_level_name'] == '非常高') & (
            data_fit_group_transform_IQR_filter[
                'correlation'] == -1)].shape[
    0] > 0:
    data_fit_group_transform_IQR_filter.ix[(data_fit_group_transform_IQR_filter['abnormal_level_name'] == '非常高') & (
        data_fit_group_transform_IQR_filter['correlation'] == -1), 'monitor_result_normalize'] = MinMaxScaler(
        feature_range=(-0.5, 0.5)).fit_transform(np.array(data_fit_group_transform_IQR_filter.ix[(
                                                                                                     data_fit_group_transform_IQR_filter[
                                                                                                         'abnormal_level_name'] == '非常高') & (
                                                                                                     data_fit_group_transform_IQR_filter[
                                                                                                         'correlation'] == -1), 'monitor_result']).reshape(
        -1, 1)
    ) * (-40) + 20

# MinMaxScaler(feature_range=(-0.5,0.5)).fit_transform(
# data_fit_group_transform_IQR_filter.loc[:, 'monitor_result']) * 80+60


# 处理IQR为0数据，默认将结果置为60，将异常等级置为
data_fit_group_transform_IQR.loc[:, 'monitor_result'] = 60
data_fit_group_transform_IQR.loc[:, 'monitor_result_normalize'] = 60
data_fit_group_transform_IQR.loc[:, 'abnormal_level_name'] = '无波动'
data_fit_group_transform_final = data_fit_group_transform_IQR_filter.append(data_fit_group_transform_IQR)

# print(data_fit_group_transform_final.head(10))

# print(data_fit_group_transform_final.head(1))
# print(data_fit_group_transform_final.round({'monitor_result_normalize': 2}).head(1))
# print(data_fit_group_transform_final.dtypes)
# data_fit_group_transform_final['monitor_result_normalize']=np.round(data_fit_group_transform_final['monitor_result_normalize'],3)
# print(np.round(data_fit_group_transform_final['monitor_result_normalize'], 3).head(10))
# data_fit_group_transform_final.round({'monitor_result_normalize': 2})
# print(data_fit_group_transform_final['monitor_result_normalize'].head(100))

data_fit_group_transform_final.to_csv('D:/1.csv')


# print(data_fit_group_transform_result.head(10))
# data_group['IQR']= np.percentile(data_group['target_list'].values,0.75)
# data_group['IQR']= np.percentile(data_group['target_list'].values,0.75)-np.percentile(data_group['target_list'],0.25)

# print(data_group.head(10))



# print(data_group_area)

# for area_x in area:
# ,'shop_brand_name','first_category','target'


# data_group = pd.DataFrame(data.groupby(['aera_region','province_name','city_name']).apply(lambda x: list(x.valid_cnt)))
# data_group.columns =['aera_region','province_name','city_name','target_list']
# data_group=data.groupby(['aera_region','province_name','city_name']).valid_cnt.apply(list).to_frame('target_list')
