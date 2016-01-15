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
        collection = spider.name
        exist_list = []
        for row in self.db[collection].find({}, {'id': True}):
            exist_list.append(row['id'])  # get all existing id
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid and (item['id'] not in exist_list):
            self.db[collection].insert(dict(item))
            log.info("%s added to MongoDB database!" % collection)
        return item
