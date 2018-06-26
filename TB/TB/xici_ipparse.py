__author__ = 'Mak'

import copy
import requests
from lxml import etree

class Xici():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        self.proxy = list()
        self.pagetest = 'http://www.customs.gov.cn/publish/portal119/tab71012/info887774.htm'

    def request(self):
        for i in range(2):
            urls = "http://www.xicidaili.com/nn/{0}/".format(i+1)
            r = requests.get(urls, headers=self.headers)
            html = etree.HTML(r.text)
            table = html.xpath("//table[@id='ip_list']")[0]  # 定位那个装满IP的大框
            trs = table.xpath("//tr")[1:]  # 过滤掉第一行的标题栏  国家 IP地址 端口 服务器地址 是否匿名 类型 速度 连接时间 存活时间 验证时间

            for tr in trs:
                ip = tr.xpath("td[2]/text()")[0]
                port = tr.xpath("td[3]/text()")[0]
                PROXY = "http://" + ip + ":" + port
                print(PROXY)
                self.proxy.append(PROXY)
        P1 = self.proxy
        return P1

    def check(self, L):
        Proxy1 = copy.deepcopy(L)         #深拷贝
        cnt = 0
        for ip in L:
            proxies = {
                'http': ip
            }
            try:
                req = requests.get(self.pagetest, timeout=2, proxies=proxies, headers=self.headers)
                print(req.status_code)
                html = etree.HTML(req.text)
                aa = html.xpath('//div[@class="xl_font"]/em/a[1]/text()')
            except:
                cnt+=1
                Proxy1.remove(ip)
                print("connect failed!",cnt)
        return Proxy1

    @classmethod
    def run(cls):
        P1 = cls().request()
        print(len(P1))
        Proxy = cls().check(P1)
        print(Proxy)
        return Proxy

A = Xici.run()
print (A)