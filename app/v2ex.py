# 领取 v2ex 金币, 翻译自 https://github.com/itsmikej/V2EX-Script
from cobweb.downloader import *
import re


class V2ex:
    def __init__(self):
        self.downloader = Downloader()
        self.header = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Origin': 'https://www.v2ex.com',
            'Host': 'www.v2ex.com'
        }
        self.login_url = 'https://www.v2ex.com/signin'
        self.coin_url = 'https://www.v2ex.com/mission/daily'

    def run(self, u, p):
        login_html = self.downloader.get(self.login_url, self.header, True, timeout=5)
        print('Get once code...')
        pattern = re.compile(r'value="(\d{5})" name="once"')
        ret = pattern.findall(login_html)
        if not ret:
            print('Get once error')
            return False

        print('Login...')
        index_html = self.login(u, p, ret[0])
        if not index_html:
            print('Login error')
            return False
        print('Login success')

        self.header['Referer'] = "https://www.v2ex.com/"
        login_html = self.downloader.get(self.coin_url, self.header, True, timeout=5)
        pattern = re.compile(r"/mission/daily/redeem\?once=(\d{5})")
        ret = pattern.search(login_html)
        if not ret:
            print('v2ex changed')
            return False

        print('Get coin...')
        res_html = self.get_coin(ret.group())
        if not re.search(re.compile('每日登录奖励已领取'), res_html):
            print('Get coin error')
            return False

        print('Done~')

    def login(self, u, p, once):
        values = {
            'u': u,
            'p': p,
            'once': once,
            'next': '/'
        }
        self.header['Referer'] = self.login_url
        return self.downloader.post(self.login_url, values, self.header, True, timeout=5)

    def get_coin(self, url_part):
        url = "https://www.v2ex.com" + url_part
        self.header['Referer'] = self.coin_url
        return self.downloader.get(url, self.header, True, timeout=5)


v = V2ex()
v.run('jiangyang33@hotmail.com', 'mike19910903joy!')
