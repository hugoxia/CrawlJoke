# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

import logging as log
from scrapy.exceptions import DropItem
from crawl import settings


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
        self.db = connection[settings.MONGODB_DB]

    def process_item(self, item, spider):
        name = spider.name
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.db[name].insert(dict(item))
            log.info("%s added to MongoDB database!" % name)
        return item
