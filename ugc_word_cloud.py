# write on 2017/04/18 by SunChuan
import os

import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

font = os.path.join(os.path.dirname(__file__), 'DroidSansFallback.ttf')
print(os.path.dirname(__file__))

text_from_file_with_apath = open('D:/PycharmProjects/data/ugc/用户评价.txt', encoding='utf-8').read()

wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=True)
wl_space_split = " ".join(wordlist_after_jieba)
print(wl_space_split[:100])
my_wordcloud = WordCloud( width=800, height=400, font_path=font).generate(wl_space_split)
# print(my_wordcloud[:100])
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
