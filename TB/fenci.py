# -*- coding utf-8 -*-
__author__ = 'Maybe'

import requests
from lxml import etree

pagetest = 'http://www.customs.gov.cn/publish/portal119/tab71012/info887774.htm'
req = requests.get(pagetest, timeout=1)
html = etree.HTML(req.text)
aa = html.xpath('//div[@class="xl_font"]/em/a[1]/text()')
print(aa)