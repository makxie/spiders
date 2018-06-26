# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TbPipeline(object):
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:123456@192.168.88.1:3306/pa?charset=utf8')
        self.DBSession = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):

        return item
