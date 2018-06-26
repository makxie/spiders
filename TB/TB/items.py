# -*- coding: utf-8 -*-

# Define here the Models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,Join,TakeFirst


class TbItem(scrapy.Item):
    model = scrapy.Field()
    productname = scrapy.Field()
    shopname = scrapy.Field()
    brand = scrapy.Field()
    score = scrapy.Field()
    title = scrapy.Field()
    sellcount = scrapy.Field()
    reviewcount = scrapy.Field()
    newp = scrapy.Field()
    promoprice = scrapy.Field()
    ratescore = scrapy.Field()
    rank = scrapy.Field()
    url = scrapy.Field()


# class ipItem(scrapy.Item):
#     model = scrapy.Field()
#     productname = scrapy.Field()
#     shopname = scrapy.Field()
#     brand = scrapy.Field()
#     score = scrapy.Field()
#     title = scrapy.Field()
#     sellcount = scrapy.Field()
#     reviewcount = scrapy.Field()
#     newp = scrapy.Field()
#     promoprice = scrapy.Field()
#     ratescore = scrapy.Field()
#     rank = scrapy.Field()
#     url = scrapy.Field()