# URL 管理器
# TODO 非内存实现 mysql redis...


class UrlManager:
    # 内存
    strategy = 'default'

    def __init__(self, urls_wait=[]):
        # 等待抓取的 URL
        self.urls_wait = urls_wait
        # 已经抓取的 URL
        self.urls_done = []

    # 取一个待爬的 URL
    def get_wait_url(self):
        if len(self.urls_wait) == 0:
            return False
        return self.urls_wait[0]

    # 添加一个新的 URL
    def add_new(self, urls):
        if type(urls) == str:
            urls = [urls]
        # if type(urls) == list:
        if isinstance(urls, list):
            for url in urls:
                # TODO check url
                if not self.has(url):
                    self.urls_wait.append(url)
                else:
                    # TODO log
                    pass
        else:
            return False
        return True

    # 未爬 -> 已爬
    def move(self, url):
        if url in self.urls_wait:
            self.urls_wait.remove(url)
        self.urls_done.append(url)

    # 检查是都已经抓取 或 已经在抓取列表中
    def has(self, url):
        if url in self.urls_done or url in self.urls_wait:
            return True
        else:
            return False
