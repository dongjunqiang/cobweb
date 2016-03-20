# 下载器
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import gzip


class Downloader(object):

    def get(self, url, header={}, cookie=False, timeout=2):
        if cookie:
            self.init_cookie()

        request = urllib.request.Request(url, headers=header, method='GET')
        response = urllib.request.urlopen(request, timeout=timeout)
        data = response.read()

        return data

    def post(self, url, values, header={}, cookie=False, timeout=2):
        if cookie:
            self.init_cookie()

        values = urllib.parse.urlencode(values).encode(encoding='utf8')
        request = urllib.request.Request(url, values, header, method='POST')

        response = urllib.request.urlopen(request, timeout=timeout)
        res = response.read()

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
