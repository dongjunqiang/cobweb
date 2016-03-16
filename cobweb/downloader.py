# 下载器

import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import gzip
from urllib.error import URLError, HTTPError


class Downloader(object):

    def get(self, url, header={}, cookie=False, timeout=2):
        if cookie:
            self.init_cookie()

        try:
            request = urllib.request.Request(url, headers=header, method='GET')
            response = urllib.request.urlopen(request, timeout=timeout)
            data = response.read()
        except URLError as e:
            return False

        return data

    def post(self, url, values, header={}, cookie=False, timeout=2):
        if cookie:
            self.init_cookie()

        values = urllib.parse.urlencode(values).encode(encoding='utf8')
        request = urllib.request.Request(url, values, header, method='POST')

        try:
            response = urllib.request.urlopen(request, timeout=timeout)
            res = response.read()
        except URLError as e:
            return False

        return res

    @staticmethod
    def init_cookie():
        cookie = http.cookiejar.CookieJar()
        # 创建cookie处理器
        cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
        # 构建opener
        opener = urllib.request.build_opener(cookie_handler, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)

    @staticmethod
    def ungzip(data):
        try:
            un_data = gzip.decompress(data)
        except TypeError:
            return data
        return un_data
