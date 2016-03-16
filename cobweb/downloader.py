# 下载器

import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import gzip
from urllib.error import URLError, HTTPError


class Downloader(object):
    
    cookeObj = None

    def get(self, url, header={}, cookie=False):
        if cookie:
            self.init_cookie()
        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            data = response.read()
        except URLError as e:
            return False

        if cookie:
            self.save_cookie()

        return data

    def post(self, url, values, header={}, cookie=False):
        if cookie:
            self.init_cookie()

        values = urllib.parse.urlencode(values).encode(encoding='utf8')
        request = urllib.request.Request(url, values, header)

        try:
            # response = opener.open(request, timeout=5)
            response = urllib.request.urlopen(request, timeout=5)
            res = response.read()
        except URLError as e:
            return False

        if cookie:
            self.save_cookie()
        return res

    def init_cookie(self):
        cookie = self.get_cookie_obj()
        # 读取cookie到变量
        try:
            cookie.load(self.get_cookie_file(), ignore_discard=True, ignore_expires=True)
        except OSError as e:
            pass
        # 创建cookie处理器
        cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
        # 构建opener
        opener = urllib.request.build_opener(cookie_handler, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)

    def save_cookie(self):
        cookie = self.get_cookie_obj()
        cookie.save(self.get_cookie_file(), ignore_discard=True, ignore_expires=True)

    def get_cookie_obj(self):
        if not self.cookeObj:
            self.cookeObj = http.cookiejar.MozillaCookieJar()
        return self.cookeObj

    @staticmethod
    def ungzip(data):
        try: 
            data = gzip.decompress(data)
        except:
            pass
        return data

    @staticmethod
    def get_cookie_file():
        return '/tmp/cookie.txt'


'''
v = {
    'client_id': 15,
    'uid': 100
}
header = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Referer': 'http://www.zhihu.com/articles'
}
d = Downloader()
data = d.get('http://www.baidu.com/', header, True)
print(data)
'''
