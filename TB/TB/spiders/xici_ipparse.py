__author__ = 'Mak'

import scrapy
import requests
from TB.items import ipItem
from scrapy.loader import ItemLoader

class XiciSpider(scrapy.Spider):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    name = "xici"
    allowed_domains = ["xicidaili.com", ]

    def start_requests(self):
        for i in range(100):
            urls = "http://www.xicidaili.com/nn/{0}/".format(i+1)
            yield scrapy.Request(urls, callback=self.parse, headers=self.headers)

    def parse(self, response):
        table = response.xpath("//table[@id='ip_list']")[0]  # 定位那个装满IP的大框
        trs = table.xpath("//tr")[1:]  # 过滤掉第一行的标题栏  国家 IP地址 端口 服务器地址 是否匿名 类型 速度 连接时间 存活时间 验证时间
        for tr in trs:
            pagetest = "http://www.baidu.com.cn/"  # 用于测试的网页
            ip = tr.xpath("td[2]/text()").extract()[0]
            port = tr.xpath("td[3]/text()").extract()[0]
            PROXY = "http://" + ip + ":" + port
            proxies = {
                "http": PROXY
            }
            try:
                response = requests.get(pagetest, timeout=1, proxies=proxies)
                print(response.status_code)
                if response.status_code == 200:  # 判断返回的状态代码来判断IP是否可用
                    yield {
                        'ip': ip,
                        'port': port,
                    }
            except:
                print("connect failed!")