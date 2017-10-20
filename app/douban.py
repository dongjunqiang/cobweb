# -*- coding=utf-8 -*-
import sys
sys.path.append("..")
from cobweb.downloader import *
from bs4 import BeautifulSoup
import re


class Douban:
    def __init__(self):
        self.area = ""
        self.pages = 10
        self.pagesize = 25
        self.url_map = [
            ["https://www.douban.com/group/zhufang/discussion", "北京无中介租房"],
            ["https://www.douban.com/group/beijingzufang/discussion", "北京租房"],
            ["https://www.douban.com/group/26926/discussion", "北京租房豆瓣"]
        ]
        self.downloader = Downloader()
        self.header = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Host': 'www.douban.com',
            'Referer': 'https://www.douban.com/group/explore',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
        }

    def parse(self, html):
        ret = []
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find_all("table", class_="olt")
        if not table:
            print("can not find table")
            return False

        tr_list = table[0].find_all("tr", class_="")
        if not tr_list:
            print("can not find tr")
            return False

        for tr in tr_list:
            td_list = tr.find_all("td")
            p = re.compile('<td class="title">.*<a class="" href="(.*)" title="(.*)">.*</td>'
                           ', <td nowrap="nowrap"><a.*>(.*)</a></td>'
                           ', <td class="" nowrap="nowrap">(.*?)</td>'
                           ', <td class="time" nowrap="nowrap">([-\d\s:]*?)</td>', re.S)
            res = p.findall(str(td_list))
            if res:
                url = res[0][0]
                title = res[0][1]
                name = res[0][2]
                comment = res[0][3]
                time = res[0][4]
                for area in self.area:
                    if area in title:
                        ret.append("标题: %s\n地址: %s\n留言: %s\n用户: %s\n时间: %s" % (title, url, comment, name, time))
            else:
                print("re fail")
        return ret

    def search(self):
        print("请输入区域,多个词用逗号分割:")
        area = input()
        if not area:
            print("未输入内容!")
            exit()

        self.area = area.split(",")
        for url_conf in self.url_map:
            base_url = url_conf[0]
            for page in range(self.pages):
                url = "%s?start=%d" % (base_url, page*self.pagesize)
                print("[%s] 第%d页 %s" % (url_conf[1], page+1, url))
                html_doc = None
                i = 0
                while True:
                    i += 1
                    if i >= 3:
                        break
                    try:
                        html_doc = self.downloader.get(url=url, header=self.header)
                        break
                    except Exception as e:
                        print("请求发生异常:%s 重试第%d次" % (str(e), i))
                # with open("../data/douban.txt", "r", encoding="utf-8") as f:
                #     html_doc = f.read()
                if not html_doc:
                    continue
                ret = self.parse(html_doc)
                if ret:
                    print("%s\n" % "\n-----------------\n".join(ret))
                else:
                    print("本页木有 '%s' 的相关结果\n" % "|".join(self.area))


if __name__ == "__main__":
    Douban().search()
