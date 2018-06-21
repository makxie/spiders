# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,Join,TakeFirst


class TbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ipItem(scrapy.Item):
    #西刺代理池

    ip = scrapy.Field()
    port = scrapy.Field()
    address = scrapy.Field()
    type = scrapy.Field()
    protocol = scrapy.Field()
    speed = scrapy.Field()
    time = scrapy.Field()
    alive = scrapy.Field()
    proof = scrapy.Field()