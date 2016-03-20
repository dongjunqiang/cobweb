# 调度器
from .parser import *
from .urlManager import *
from .downloader import *
from .storage import *
from .logger import *
from urllib.parse import urlparse
from urllib.error import URLError


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
            try:
                # 下载
                html = self.downloader.get(url)
                # 解析
                self.parser.set_html(html).parse_url().parse_content()

                # 存储有用信息
                parser_url = urlparse(url)
                filename = "%s@%s.html" % (parser_url.path.replace('/', '_').strip('_'), parser_url.query.replace('=', '#'))
                # TODO 文件路径
                if not self.storage.set_base_dir('/Users/itsmikej/code/python/Cobweb/data/')\
                        .save(filename, self.parser.get_content()):
                    self.logger.do_log_simple("url[%s] pass" % url)
                    pass

                # 解析出新 url
                urls = self.parser.get_url()
                # 加入到管理器
                self.urlManager.add_new(urls)
                # 移动 url 到已抓取
                self.urlManager.move(url)
                self.logger.do_log_simple("url[%s] done" % url)
                url = self.urlManager.get_wait_url()
            except URLError as e:
                self.logger.do_log_simple("URLError: %s" % str(e))
                pass
