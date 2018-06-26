# -*- coding:utf-8 -*-
__author__ = 'Maybe'

from scrapy import Request
import time, re
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from lxml import etree


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
        name = '电饭煲'
        input.send_keys(name)
        input.send_keys(Keys.ENTER)
        """
        点击查看所有宝贝
        """
        button_total = browser.find_element_by_xpath('//a[@class="total link"]')
        button_total.click()
        # """
        # 选择品类下的品牌
        # """
        # button = browser.find_element_by_xpath('//div[@class="foot"]/span[@class="switch-multi J_OpenMulti"]')
        # button.click()
        # button_midea = browser.find_element_by_xpath('//div[@id="J_NavCommonRowItems_0"]/a[@title="美的"]')
        # button_jiuyang = browser.find_element_by_xpath('//div[@id="J_NavCommonRowItems_0"]/a[@title="九阳"]')
        # button_supor = browser.find_element_by_xpath('//div[@id="J_NavCommonRowItems_0"]/a[@title="苏泊尔"]')
        # button_midea.click()
        # button_jiuyang.click()
        # button_supor.click()
        # time.sleep(1)
        # """提交"""
        # button_sub = browser.find_element_by_xpath('//div[@id="J_NavCommonRow_0"]/div[2]/div[2]/span[1]')
        # button_sub.click()
        # time.sleep(3)
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
            for i in range(1, 2):
                num = 1+i
                link = Selector(text=html).xpath('//div[@class="grid g-clearfix"]/div/div['+str(num)+']/div[2]/div[2]/a/@href').extract()
                Urls.append(link[0])

            button_next = browser.find_element_by_xpath('//li[@class="item next"]/a')
            button_next.click()
            time.sleep(3)
        print(Urls)
        print('--------------------结束链接爬取----------------------')
        browser.close()

        rank = 0
        for url_1 in Urls:
            rank += 1
            # meta = {
            #     'dont_redirect': True,  # 禁止网页重定向
            #     'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
            # }
            url = 'https:'+url_1
            yield Request(url, callback=self.parse, headers=self.headers, dont_filter=True, meta={'rank': rank,
                                                                                                  'url': url,
                                                                                                  'productname': name})

    def parse(self, response):
        #天猫
        if 'tmall' in str(response.meta['url']):
            content = response.text
            html = etree.HTML(content)
            """正则部分"""
            pattern_model = re.compile(r'型号</th><td>&nbsp;(.*?)</td>')
            pattern_productname = re.compile(r'>产品名称：(.+)<')
            pattern_shopname = re.compile(r'data-spm="d4918089"><strong>(.+?)</')
            pattern_brand = re.compile(r'品牌:&nbsp;(.+?);</')
            pattern_score = re.compile(r'shopdsr-score-con">(.+?)</')

            model = re.findall(pattern_model, content)[0]
            productname = re.findall(pattern_productname, content)[0]
            shopname = re.findall(pattern_shopname, content)[0]
            brand = re.findall(pattern_brand, content)[0]
            score = re.findall(pattern_score, content)

            """xpath部分"""
            title = html.xpath('//h1[@data-spm="1000983"]/a/text()')[0]
            """调用webdriver爬取,并设置代理"""
            browser = webdriver.Chrome()
            # options = webdriver.ChromeOptions()
            # options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"')
            # options.add_argument('--proxy-server=http://122.114.31.177:8080')
            # browser = webdriver.Chrome(chrome_options=options)
            browser.get(response.meta['url'])
            #下拉
            js = "var q=document.documentElement.scrollTop=10000"
            browser.execute_script(js)
            time.sleep(2)
            html_sele = etree.HTML(browser.page_source)
            sellcount = html_sele.xpath('//li[@data-label="月销量"]/div/span[2]/text()')[0]
            reviewcount = html_sele.xpath('//li[@class="tm-ind-item tm-ind-reviewCount canClick tm-line3"]/div/span[2]/text()')[0]
            newp = html_sele.xpath('//div[@class="tb-detail-hd"]/p/text()')[0]
            promoprice = html_sele.xpath('//div[@class="tm-promo-price"]/span/text()')[0]
            button_comment = browser.find_element_by_xpath('//ul[@class="tabbar tm-clear"]/li[3]')
            button_comment.click()
            time.sleep(2)
            """下拉后获取到评论小界面提取"""
            pattern_comment = re.compile(r'title="(.+)分')
            content = browser.page_source
            ratescore = re.findall(pattern_comment, content)[0]
            browser.quit()

            items = dict()
            items['model'] = model
            items['productname'] = productname
            items['shopname'] = shopname
            items['brand'] = brand
            items['score'] = score
            items['title'] = title
            items['sellcount'] = sellcount
            items['reviewcount'] = reviewcount
            items['newp'] = newp
            items['promoprice'] = promoprice
            items['ratescore'] = ratescore
            items['rank'] = response.meta['rank']
            items['url'] = response.meta['url']
            for item in items.items():
                print(item)
        else:
            items = dict()
            browser = webdriver.Chrome()
            browser.get(response.meta['url'])
            time.sleep(2)
            html = etree.HTML(browser.page_source)
            browser.quit()

            model = html.xpath('//ul[@class="attributes-list"]/li[4]/text()')
            brand = html.xpath('//ul[@class="attributes-list"]/li[3]/text()')
            shopname = html.xpath('//div[@class="tb-shop-name"]/dl/dd/strong/a/text()')
            title = html.xpath('//h3[@class="tb-main-title"]/text()')
            sellcount = html.xpath('//div[@class="tb-sell-counter"]/a/strong/text()')
            reviewcount = html.xpath('//div[@class="tb-rate-counter"]/a/strong/text()')
            score = html.xpath('//dd[@class="tb-rate-lower"]/a/text()')
            promoprice = html.xpath('//strong[@class="tb-promo-price"]/em[2]/text()')

            items['model'] = model
            items['productname'] = response.meta['productname']
            items['shopname'] = shopname
            items['brand'] = brand
            items['score'] = score
            items['title'] = title
            items['sellcount'] = sellcount
            items['reviewcount'] = reviewcount
            items['newp'] = ''
            items['promoprice'] = promoprice
            items['ratescore'] = ''
            items['rank'] = response.meta['rank']
            items['url'] = response.meta['url']
            for item in items.items():
                print(item)




