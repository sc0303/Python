#!/usr/bin/env python
# -*- coding: gbk -*-
import os
# import codes
import re
import numpy as np
import pandas as pd
from pandasql import sqldf
import chardet
import jieba
import logging
import jieba.analyse
from impala.dbapi import connect
from gensim import corpora, models, similarities

pysqldf = lambda q: sqldf(q, globals())

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# ͣ�ʺ�ͣ�ʱ�־�Ĵ���
# ͣ��
f = open('C:/Users/chuan.sun/Desktop/stopwords/stop_words_zh_UTF-8.txt', 'r', encoding='utf8')
stopwords = f.readlines()
f.close()
stopwords = [w.strip() for w in stopwords]
# ͣ�ʱ�־
stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']

# �޳������쳣�ַ�
punctuations = [',', '.', '/', ';', ':', '"', '[', '{', ']', '}', '?', '`', '~', '!', '@', '#', '$', '%', '����',
                '&',
                '*', '(', ')', '-', '����', '+', '=', '��', '��', '/', '��', '��', '<', '>', '��', '��', '��', '��', '��', '��',
                '{', '��', '}', '��', '|', '~', '��', ' @ ', '  # ', '��', '%', '����', '&', '*', '��', '��', '-', '����', '=',
                '+']


# def tokenization(food_name):
#     result = []
#     words = jieba.cut(str(food_name), cut_all=True)
#     for word, flag in words:
#         if flag not in stop_flag and word not in stopwords:
#             result.append(word)
#     return result

def tokenization(food_name):
    result = []
    words = jieba.cut(str(food_name), cut_all=False)
    for word in words:
        if word not in stopwords:
            result.append(word)
    return result


# # ���������Լ����ݲ�ѯ
conn = connect(host='10.0.250.104', port=10001, user='analyst_user', auth_mechanism='PLAIN', password='dt@ele.me',
               database='temp')
#
# # �̻��̻���Ӧ�Ĳ�Ʒ��Ϣ
# cursor1 = conn.cursor()
# cursor1.execute(
#     'select restaurant_id, name from temp.temp_shop_similarity_meituan_food_info where restaurant_id = 454936 and month_sold_count > 0')
# df_shangji_input = pd.DataFrame([x for x in cursor1], columns=['restaurant_id', 'name'])
#
# print(df_shangji_input.head(10))
#
# # ���Ʋ�����Ӧ�Ĳ�Ʒ��Ϣ
# cursor2 = conn.cursor()
# cursor2.execute(
#     'select input_shop_id,restaurant_id, name from temp.temp_shop_similarity_meituan_shop_first_step_filter_food')
# df_shangji_similarity_input = pd.DataFrame([x for x in cursor2], columns=['input_shop_id', 'restaurant_id', 'name'])
#
# # �����̻��̻�id
# cursor3 = conn.cursor()
# cursor3.execute('select 454936')

# д�����Ʋ�������
cursor4 = conn.cursor()

# ʹ��csv�ĵ�ģ��hive����
df_shangji_input = pd.read_excel('C:/Users/chuan.sun/Desktop/rst_similarity/input_shop.xlsx',
                                 columns=['restaurant_id', 'name'])
df_shangji_similarity_input = pd.read_excel('C:/Users/chuan.sun/Desktop/rst_similarity/similarity_shop.xlsx',
                                            columns=['input_shop_id', 'restaurant_id', 'name'])

# ÿ��ѭ������һ���̻����ƶ�
cursor3 = [454936]

# �����������
similarity_rst_output = []
for shop_id in cursor3:

    # �ռ����е����̻���Ʒ����,�����в�Ʒ������һƪ���½��д���
    shangji_food_tmp = pysqldf(
        'select name from df_shangji_input where restaurant_id=%d' % shop_id).values.tolist()
    shangji_food_tmp = np.array(shangji_food_tmp).flatten().tolist()

    # ȥ���̻���Ʒ�е�����˵��
    a1 = re.compile('\��.*\��|\��.*\��|\(.*\)|\{.*\}')
    shangji_food = [a1.sub('', x) for x in shangji_food_tmp]
    print(shangji_food)
    shangji_food_after_cut = tokenization(shangji_food)
    print(shangji_food_after_cut)

    # �ռ������̻����Ʋ����Ĳ�Ʒ
    shangji_similarity_food_tmp = pysqldf(
        'select distinct restaurant_id,name from df_shangji_similarity_input where input_shop_id =%d' % shop_id).values.tolist()
    shangji_similarity_rst_num = int(pysqldf(
        'select count(distinct restaurant_id) from df_shangji_similarity_input where input_shop_id =%d' % shop_id).values)

    # ��Ʒ���̻�id��ӳ���ϵ�����һ��dict
    similarity_rst_dict = {}
    similarity_food_list = [[] for i in range(0, shangji_similarity_rst_num)]
    rst_num = 0
    for i in range(0, len(shangji_similarity_food_tmp)):
        rst_id = shangji_similarity_food_tmp[i][0]
        if rst_id not in similarity_rst_dict:
            similarity_rst_dict[rst_id] = rst_num
            rst_num = rst_num + 1
        similarity_food_list[rst_num - 1].append(a1.sub('', shangji_similarity_food_tmp[i][1]))  # ȥ�������̻���Ʒ�е�����˵��

    # �������̻���Ʒ���ִ�
    similarity_food_after_cut = []
    for each in similarity_food_list:
        similarity_food_after_cut.append(tokenization(each))

    # print(similarity_food_after_cut)
    # ���ɴʴ�
    dictionary = corpora.Dictionary(similarity_food_after_cut)

    # ���ִʺ�Ĳ�Ʒ����ӳ��Ϊ����
    doc_vectors = [dictionary.doc2bow(text) for text in similarity_food_after_cut]

    tfidf = models.TfidfModel(doc_vectors)
    tfidf_vectors = tfidf[doc_vectors]

    # ������̻���Ʒ����
    query = shangji_food_after_cut
    query_bow = dictionary.doc2bow(query)
    index = similarities.MatrixSimilarity(tfidf_vectors)
    sims = index[query_bow]
    sims = list(enumerate(sims))

    # ����������������
    sims_sorted = sorted(sims, key=lambda x: x[1])


    similarity_rst_output.append([shop_id, list(similarity_rst_dict.keys())[
        list(similarity_rst_dict.values()).index(sims_sorted[-1][0])],sims_sorted[-1][1]])
    similarity_rst_output.append(
        [shop_id,
         list(similarity_rst_dict.keys())[list(similarity_rst_dict.values()).index(sims_sorted[-2][0])],sims_sorted[-2][1]])
    similarity_rst_output.append(
        [shop_id,
         list(similarity_rst_dict.keys())[list(similarity_rst_dict.values()).index(sims_sorted[-3][0])],sims_sorted[-3][1]])
    print(similarity_rst_output)

# ������Ʋ����������
pd.DataFrame(similarity_rst_output, columns = ['input_shop_id', 'similarity_shop_id','similarity']).to_csv(
    'C:/Users/chuan.sun/Desktop/rst_similarity/similarity_rst_output.csv', index=False, header=True)




# print(list(similarity_rst_dict.keys())[list(similarity_rst_dict.values()).index(sims_sorted[0][0])])
# for key, value in similarity_rst_dict.iteritems():
#     if value == sims_sorted[-1][0]:
#         print(key)

# cursor3.execute('drop table if exists temp.temp_shop_similarity_meituan_shop_info;
# create table temp.temp_shop_similarity_meituan_shop_info as')


# # cursor4.execute('INSERT INTO temp.new_table_test_chuan_sun_pandas VALUES ('', 2005-02-12, 3)')
#
# sql = "INSERT into temp.new_table_test_chuan_sun_pandas VALUES (%s, %s,%s)"
# row = [ "12345", 1,2]
# cursor4.execute((sql), (row))
#
# # INSERT INTO Persons (LastName, Address) VALUES ('Wilson', 'Champs-Elysees')


# lsi�Ĵ��������Ǻ����룬��Ҫԭ��Ϊ��Ʒƥ�������Ҫ���ݹؼ��ʽ���ƥ�䣬���ǰ���������˼����ƥ��
# lsi = models.LsiModel(tfidf_vectors, id2word=dictionary, num_topics=len(similarity_rst_dict))
# lsi_vector = lsi[tfidf_vectors]
# query_lsi = lsi[query_bow]
# index_lsi = similarities.MatrixSimilarity(lsi_vector)
# sims_lsi = index[query_lsi]
# sims_lsi = list(enumerate(sims_lsi))
# sims_lsi_sorted = sorted(sims_lsi, key=lambda x: x[1])
# print(list(similarity_rst_dict.keys())[list(similarity_rst_dict.values()).index(sims_lsi_sorted[-1][0])])
# print(list(similarity_rst_dict.keys())[list(similarity_rst_dict.values()).index(sims_lsi_sorted[0][0])])

# shangji_similarity_food_tmp = np.array(shangji_similarity_food_tmp).flatten().tolist()

# print(pysqldf('select name from df_shangji_input where restaurant_id=%d' %shop_id))
# shangji_food = list(pysqldf('select name from df_shangji_input where cast(restaurant_id as bigint) =454936' ))
# print(shangji_food)



# for row in cursor1:
#     meituan_food.append(row[1])
#
#     # �ռ�����de�̻����Ʋ�Ʒ���ϣ������в�Ʒ������һƪ���½��д���
#
# df_tmp = pysqldf('select 123')
#
#
#
# meituan_food_filter_stop_words = []
# words = jieba.cut(str(meituan_food), cut_all=True)
# for word, flag in words:
#     print(word)
# print(flag)
# if flag not in stop_flag and word not in stopwords:
#     meituan_food_filter_stop_words.append(word)
#
# meituan_food_after_jieba = jieba.cut(str(meituan_food), cut_all=True)
#
# print(meituan_food)
# print(meituan_food_after_jieba)
#
# texts_filtered = [
#     [food_filter_punctuations for food_filter_punctuations in document if not food_filter_punctuations in punctuations]
#     for document in meituan_food]
#
# print(texts_filtered)

# ��¼��ģ�����е���־



# [[word for word in document if not word in english_punctuations] for document in texts_filtered_stopwords]

# print(jieba.analyse.extract_tags(str(meituan_food_after_jieba), topK=5, withWeight=False, allowPOS=()))


# print(cursor.description)
# print(cursor.fetchall())


# text_from_file_with_apath = open('D:/PycharmProjects/data/ugc/�û�����.txt', encoding='utf-8').read()
#
# wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=True)
