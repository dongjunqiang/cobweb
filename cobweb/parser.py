# 解析器
import types
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Parser:
    def __init__(self, func_parse_url=None, func_parse_content=None):
        self.html = None
        self.soup = None
        self.content = None
        self.urls = []
        self.base_url = None
        self.filter_str_list = []

        # 自定义解析器
        if func_parse_url is not None:
            self.parse_url = types.MethodType(func_parse_url, self)

        if func_parse_content is not None:
            self.parse_content = types.MethodType(func_parse_content, self)

    # 解析内容
    def parse_content(self):
        self.content = self.soup.body

    # 解析 url
    def parse_url(self):
        node = self.soup.find_all('a')
        for n in node:
            url = self.filter_url(n.get('href', ''))
            if url:
                self.urls.append(url)

    # 过滤url
    def filter_url(self, url):
        parse_url = urlparse(url)
        if not url:
            return False
        elif url == '/' or url == '#' or 'javascript:' in url:
            return False
        # 判断 scheme
        elif parse_url.scheme and parse_url.scheme != self.base_url.scheme:
            return False
        # 判断 url 是否属于当前域名
        elif parse_url.netloc and parse_url.netloc not in self.base_url.netloc:
            return False

        if self.filter_str_list:
            for str_ in self.filter_str_list:
                if str_ in url:
                    return False

        if not parse_url.netloc:
            url = 'http://' + self.base_url.netloc + url
        return url

    def set_html(self, html):
        self.html = html
        self.soup = BeautifulSoup(self.html, 'html.parser', from_encoding='utf8')

    def set_base_url(self, base_url):
        self.base_url = urlparse(base_url)

    def add_filter_str(self, filter_str):
        self.filter_str_list.append(filter_str)

    def get_content(self):
        return self.content

    def get_url(self):
        return self.urls

'''
html_ = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
</body>
"""
a = Parser()
a.set_html(html_)
a.set_base_url('http://example.com/')
a.parse_url()
a.parse_content()
print(a.get_url())
'''
