# write on 2016/06/13 by SunChuan
import urllib.request
from urllib.parse import *

from bs4 import BeautifulSoup
from sqlite3 import dbapi2 as sqlit

ignore_words = set(['the', 'to', 'of', 'and', 'is', 'it', 'in', 'a'])

class crawler:
    # 类初始化
    def __init__(self, dbname):
        self.con = sqlit.connect(dbname)

    def __del__(self):
        self.con.close()

    # 数据库连接
    def dbcommit(self):
        self.con.commit()

    # 辅助函数，用于获取用户的条目id，如果条目不存在，则将其加入数据库中
    def get_entry_id(self, table, field, value, creat_new=True):
        return None

    # 给每个网页添加索引
    def add_index(self, url, soup):
        print('index %s' % url)

    # 从一个html提取文字

    def get_txt_only(self, soup):
        v = soup.string()
        if v == None:
            c = soup.contents
            result_txt = ''
            for result in c:
                sub_txt = self.get_txt_only(result)
                result_txt += sub_txt + '\n'
            return result_txt
        else:return v.strip()


    # 根据任何非空白字符进行分次处理
    def separate_words(self, text):
        splitter = re.compile('\\W*')#没有理解这个正则表达式的含义
        return [s.lower() for s in splitter.split(text) if s != '']
    # 判断url是否建立过索引
    def is_index(self, url):
        return None

    # 添加一个关联两个网页的链接
    def add_link_ref(self, url_from, url_to, link_text):
        pass

    # 从一个小组网页开始进行广度优先搜索，直至某一给定深度
    # 期间为网页建立索引
    def crawl(self, pages, depth=2):
        for i in range(depth):
            new_page = set()
            for page in pages:
                try:
                    c = urllib.request.urlopen(page)
                except:
                    print("Can't open %s" % page)
                    continue
                soup = BeautifulSoup(c.read(), 'lxml',from_encoding='gb18030')  # 解决编码乱码的问题,编码问题是个很头痛的问题
                # with open('D:/DataMining/machinelearninginaction/test.txt', 'w', encoding='utf-8') as file:
                #     file.write(str(soup))
                # print(soup)
                self.add_index(page, soup)  # 注意这里面调用了类的对象方法，使用self.add_index()而不是调用类的私有方法add_index()
                links = soup('a')
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1: continue
                        url = url.split('#')[0]
                        if url[0:4] == 'http' and not self.is_index(url):
                            new_page.add(url)
                        link_text = self.get_txt_only(link)
                        self.add_link_ref(page, url, link_text)
                self.dbcommit()
            pages = new_page


    # 创建数据库表
    def create_table_index(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid, wordid, location)')
        self.con.execute('create table link(fromid integer, toid integer)')
        self.con.execute('create table linkwords(wordid, linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')







page_list = ['http://news.163.com/16/0620/22/BQ1ODV1J000156PO.html']
my_crawler = crawler('my_db')
# my_crawler.crawl(page_list)
my_crawler.create_table_index()


#停留在书中P83