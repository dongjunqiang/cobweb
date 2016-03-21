# 抓取嗅事百科的段子
from cobweb.downloader import *
from cobweb.parser import *
import time
import re


def parse_joke(self):
    data = self.soup.find_all('div', class_='article block untagged mb15')
    content_pattern = re.compile("<div.*?content\">(.*?)<!--(.*?)-->.*?</div>", re.S)
    self.content = []
    for d in data:
        soup_d = BeautifulSoup(str(d), 'html.parser', from_encoding='utf8')
        # 用户名
        name = soup_d.h2.string
        # 内容（内容+时间&图片）
        c = soup_d.find('div', class_='content')
        # content = str(c.contents[0]).strip('\n')
        # timestamp = str(c.contents[1])
        re1 = content_pattern.findall(str(c))
        content = re1[0][0].strip('\n').replace('<br>', '\n')
        timestamp = re1[0][1]
        img = soup_d.find('div', class_='thumb')
        if img:
            img_src = img.contents[1].contents[1]['src']
            content += "[img: %s]" % str(img_src)
        # 点赞数
        like = soup_d.find('i', class_='number').string
        j = "name: %s\ncontent: %s\ntime: %s\nlike: %s" % (str(name), content, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp))), str(like))
        self.content.append(j)
    return self


class Sxbk:
    def __init__(self):
        self.page = 1
        self.url = 'http://www.qiushibaike.com/hot/page/'
        self.joke_lists = []
        self.enable = True
        self.downloader = Downloader()
        self.parse = Parser(None, parse_joke)

    # 下载页面
    def get_page(self, num=1):
        return self.downloader.get(self.url + str(num), header={
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        }, timeout=50).decode('utf8')

    # 解析段子到 list
    def gen_jokes(self, html):
        self.parse.set_html(html)
        self.joke_lists += self.parse.parse_content().get_content()

    # start
    def start(self):
        print('按回车开始...')
        while self.enable:
            n = input()
            if n == 'q':
                exit()
            if len(self.joke_lists) < 2:
                html = self.get_page(self.page)
                self.gen_jokes(html)
                self.page += 1
            print(self.joke_lists[0])
            del self.joke_lists[0]


s = Sxbk()
s.start()
