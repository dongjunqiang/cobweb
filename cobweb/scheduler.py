# 调度器
from .parser import *
from .urlManager import *
from .downloader import *
from .storage import *
from .logger import *
from urllib.parse import urlparse


class Scheduler:
    def __init__(self):
        self.parser = Parser()
        self.urlManager = UrlManager()
        self.downloader = Downloader()
        self.storage = Storage()
        self.logger = Logger()

    # test
    def start(self, url):
        self.parser.set_base_url(url)
        while url:
            # 下载
            html = self.downloader.get(url)
            # 解析
            self.parser.set_html(html).parse_url().parse_content()

            # 存储有用信息
            filename = urlparse(url).path.replace('/', '_').strip('_') + '.html'
            if not self.storage.set_base_dir('/Users/itsmikej/code/python/Cobweb/data/')\
                    .save(filename, self.parser.get_content()):
                pass

            # 解析出新 url
            urls = self.parser.get_url()
            # 加入到管理器
            self.urlManager.add_new(urls)
            # 移动 url 到已抓取
            self.urlManager.move(url)
            self.logger.do_log_simple("url[%s] done" % url)
            url = self.urlManager.get_wait_url()
