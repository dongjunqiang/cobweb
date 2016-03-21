# 领取 v2ex 金币, 翻译自 https://github.com/itsmikej/V2EX-Script
from cobweb.downloader import *
from cobweb.logger import *
import re


class V2ex:
    def __init__(self):
        self.downloader = Downloader()
        self.logger = Logger('./')
        self.header = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Origin': 'https://www.v2ex.com',
            'Host': 'www.v2ex.com'
        }
        self.login_url = 'https://www.v2ex.com/signin'
        self.coin_url = 'https://www.v2ex.com/mission/daily'
        self.get_coin_url = 'https://www.v2ex.com/mission/daily/redeem?once='

    def run(self, u, p):
        login_html = self.downloader.get(self.login_url, self.header, True)
        self.logger.do_log_simple('Get coin code...')
        pattern = re.compile(r'value="(\d{5})" name="once"', re.S)
        code = pattern.findall(login_html)[0]
        if not self.login(u, p, code):
            return False
        self.get_coin()

    def login(self, u, p, code):
        self.logger.do_log_simple('Login...')
        values = {
            'u': u,
            'p': p,
            'once': code,
            'next': '/'
        }
        self.header['Referer'] = self.login_url
        ret = self.downloader.post(self.login_url, values, self.header, True)
        if False:
            return False
        self.logger.do_log_simple('Login success!')
        return True

    def get_coin(self):
        self.header['Referer'] = "https://www.v2ex.com/"
        coin_html = self.downloader.get(self.coin_url, self.header, True)
        pattern = re.compile(r"/mission/daily/redeem\?once=(\d{5})", re.S)
        code = pattern.findall(coin_html)[0]
        self.header['Referer'] = self.coin_url
        self.downloader.get(self.get_coin_url + str(code), self.header, True)
        self.logger.do_log_simple('Success')


v = V2ex()
v.run('***', '***')

