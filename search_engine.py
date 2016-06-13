# write on 2016/06/13 by SunChuan
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import *

class crawler:
    #类初始化
    def __init__(self, dbname):
        pass

    def __del__(self):
        pass
    #数据库连接
    def dbcommit(self):
        pass

    #辅助函数，用于获取用户的条目id，如果条目不存在，则将其加入数据库中
    def get_entry_id(self,table, field, value, creat_new = True):
        return None

    #给每个网页添加索引
    def add_index(self, url, soup):
        print('index %s' %url)

    #从一个html提取文字

    def get_txt_only(self,soup):
        return None

    #根据任何非空白字符进行分次处理
    def separate_words(self,text):
        return None

    #判断url是否建立过索引
    def is_index(self, url):
        return None

    #添加一个关联两个网页的链接
    def add_link_ref(self, url_from, url_to, link_text):
        pass

    #从一个小组网页开始进行广度优先搜索，直至某一给定深度
    #期间为网页建立索引
    def crawl(self,pages, depth = 2):
        ignore_words = set(['the', 'to', 'of', 'and','is', 'it', 'in', 'a'])
        for i in range(depth):
            new_page = set()
            for page in pages:
                try:
                    c = urllib.request.urlopen(page)
                except:
                    print("Can't open %s" %page)
                    continue
                soup = BeautifulSoup(c.read())
                self.add_index(page, soup)  #注意这里面调用了类的对象方法，使用self.add_index()而不是调用类的私有方法add_index()
                print(soup)
                links = soup('a')
                print(links)
                for link in links:
                    if('href' in dict(link.attrs)):
                        url = urljoin(page, link['href'])
                        if url.find("'")!= -1:continue
                        url = url.split('#')[0]
                        if url[0:4]=='http' and not self.is_index(url):
                            new_page.add(url)
                        link_text = self.get_txt_only(link)
                        self.add_link_ref(page, url, link_text)
            self.dbcommit()
        pages = new_page



        pass

    #创建数据库表
    def create_table_index(self):
        pass



page_list = ['http://pandas.pydata.org/pandas-docs/stable/api.html']
my_crawler = crawler('my_db')
my_crawler.crawl(page_list)

