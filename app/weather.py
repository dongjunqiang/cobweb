# -*- coding=utf-8 -*-
from cobweb.downloader import *
from bs4 import BeautifulSoup
from datetime import date, datetime
from urllib import parse
import urllib.request
import base64
import time


class Weather:
    def __init__(self, cities, save_path):
        self.cities = cities
        self.save_path = save_path
        self.downloader = Downloader()
        self.url = "https://www.aqistudy.cn/historydata/daydata.php?city=%s&month=%s"
        self.header = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Host': 'www.aqistudy.cn',
            'Referer': 'https://www.aqistudy.cn/historydata/daydata.php?city=%E6%88%90%E9%83%BD&month=201705',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
        }
        self.item_list = ['datetime', 'AQI', 'level', 'PM2_5', 'PM10', 'SO2', 'CO', 'NO2', 'O3_8h', 'rank']

    def run(self):
        if not self.cities:
            return

        for city in self.cities:
            file_name = "%s/%s.txt" % (self.save_path, city)
            f = open(file_name, "at", encoding='utf-8')
            # f.write("%s\n" % "\t".join(self.item_list))

            for day in self.jump_by_month(date(2013, 12, 1), datetime.now().date(), 1):
                year_month = "%s%s" % (day.year, str(day.month).zfill(2))
                url = self.url % (parse.quote(city), year_month)
                print("start fetch: %s" % url)

                i = 0
                while True:
                    try:
                        i = i + 1
                        html_doc = self.downloader.get(url=url, header=self.header)
                        break
                    except urllib.error.URLError:
                        print("retry %d..." % i)
                        if i >= 50:
                            exit(1)
                        time.sleep(1)
                        pass

                if html_doc:
                    data = self.parse(html_doc)
                    f.write(data)
                    print("ok")
                else:
                    print("fail")

    @staticmethod
    def jump_by_month(start_date, end_date, month_step=1):
        current_date = start_date
        while current_date < end_date:
            yield current_date
            carry, new_month = divmod(current_date.month - 1 + month_step, 12)
            new_month += 1
            current_date = current_date.replace(year=current_date.year + carry, month=new_month)

    @staticmethod
    def parse(data):
        ret = ''
        soup = BeautifulSoup(data, "html.parser")
        tr_list = soup.table.find_all('tr')
        for i, tr in enumerate(tr_list):
            if not tr.th:
                td_list = tr.find_all('td')
                line = ''
                for j, td in enumerate(td_list):

                    if j == 2:
                        if td.div.contents:
                            item = str(td.div.contents[0]).strip()
                        else:
                            item = ""
                    else:
                        item = str(td.contents[0]).strip()
                    line += "%s\t" % item

                if line:
                    ret += "%s\n" % line.strip()

        return ret

    @staticmethod
    def strtotime(string, format_string="%Y-%m-%d"):
        t_tuple = time.strptime(string, format_string)
        return int(time.mktime(t_tuple))

    def send(self):
        # ['datetime', 'AQI', 'level', 'PM2_5', 'PM10', 'SO2', 'CO', 'NO2', 'O3_8h', 'rank']
        level_map = {
            "优": 1,
            "良": 2,
            "轻度污染": 3,
            "中度污染": 4,
            "重度污染": 5,
            "严重污染": 6
        }
        point = "weather_test_1,city=%s AQI=%s,level=%d,PM2_5=%s,PM10=%s,SO2=%s,CO=%s,NO2=%s,O3_8h=%s,rank=%s %s\n"
        for city in self.cities:
            file_name = "%s/%s.txt" % (self.save_path, city)
            data = ""
            with open(file_name, 'r', encoding="utf-8") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    ll = line.strip().split("\t")
                    if ll[2] not in level_map:
                        print("wrong level", line)
                        continue

                    t = self.strtotime(ll[0])
                    data += point % (city, ll[1], level_map[ll[2]], ll[3], ll[4], ll[5], ll[6], ll[7], ll[8], ll[9], t)

                if data:
                    try:
                        request = urllib.request.Request(
                                'http://localhost:8686/write?db=test&precision=s',
                                data.strip().encode('utf-8')
                        )
                        base64string = base64.encodebytes(b'****:****').decode().replace('\n', '')
                        request.add_header("Authorization", "Basic %s" % base64string)
                        response = urllib.request.urlopen(request, timeout=5)
                        print('response:' + response.read().decode())
                    except Exception as e:
                        print('send error: ' + str(e))
                        exit()


w = Weather(['昆明'], "../data")
w.run()
# w.send()
