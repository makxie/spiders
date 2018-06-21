# -*- coding utf-8 -*-
__author__ = 'Maybe'

from scrapy import Request
import time, re
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Taobao(CrawlSpider):
    name = 'taobao'
    allowed_domains = ['detail.tmall.com']
    start_urls = [""]
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }

    def start_requests(self):
        Urls = list()
        browser = webdriver.Chrome()
        browser.get('https://www.taobao.com/')
        time.sleep(2)                           #让页面加载完
        input = browser.find_element_by_id('q')
        input.send_keys('电饭煲')
        input.send_keys(Keys.ENTER)
        """
        点击查看所有宝贝
        """
        button_total = browser.find_element_by_xpath('//a[@class="total link"]')
        button_total.click()
        """
        选择品类下的品牌
        """
        button = browser.find_element_by_xpath('//div[@class="foot"]/span[@class="switch-multi J_OpenMulti"]')
        button.click()
        button_midea = browser.find_element_by_xpath('//div[@id="J_NavCommonRowItems_0"]/a[@title="美的"]')
        button_jiuyang = browser.find_element_by_xpath('//div[@id="J_NavCommonRowItems_0"]/a[@title="九阳"]')
        button_supor = browser.find_element_by_xpath('//div[@id="J_NavCommonRowItems_0"]/a[@title="苏泊尔"]')
        button_midea.click()
        button_jiuyang.click()
        button_supor.click()
        time.sleep(1)
        button_sub = browser.find_element_by_xpath('//div[@id="J_NavCommonRow_0"]/div[2]/div[2]/span[1]')
        button_sub.click()
        time.sleep(3)
        """
        按销量排序
        """
        html = browser.page_source
        button_sale = browser.find_element_by_xpath('//a[@title="销量从高到低"]')
        button_sale.click()
        time.sleep(3)
        """
        提取商铺url
        """
        for click in range(0, 1):
            html = browser.page_source
            for i in range(0, 1):
                num = 1+i
                link = Selector(text=html).xpath('//div[@class="grid g-clearfix"]/div/div['+str(num)+']/div[2]/div[2]/a/@href').extract()
                Urls.append(link[0])

            button_next = browser.find_element_by_xpath('//li[@class="item next"]/a')
            button_next.click()
            time.sleep(3)
        print(Urls)
        print('--------------------结束链接爬取----------------------')
        browser.close()

        for url_1 in Urls:
            # meta = {
            #     'dont_redirect': True,  # 禁止网页重定向
            #     'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
            # }
            url = 'https:'+url_1
            yield Request(url, callback=self.parse, headers=self.headers, dont_filter=True)

    def parse(self, response):
        print(response.text)
        content = response.text
        pattern_model = re.compile(r'型号</th><td>&nbsp;(.*?)</td>')
        pattern_name = re.compile(r'>产品名称：(.+)<')

        model = re.findall(pattern_model, content)
        name  = re.findall(pattern_name, content)







