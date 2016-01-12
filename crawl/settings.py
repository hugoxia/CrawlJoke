# -*- coding: utf-8 -*-

# Scrapy settings for crawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawl'

SPIDER_MODULES = ['crawl.spiders']
NEWSPIDER_MODULE = 'crawl.spiders'

ITEM_PIPELINES = ['crawl.pipelines.JandanMongoDBPipeline',
                  'crawl.pipelines.PengfuMongoDBPipeline',
                  'crawl.pipelines.LaifuMongoDBPipeline',
                  'crawl.pipelines.QiubaiMongoDBPipeline']

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "crandom"

J_MONGODB_COLLECTION = "jandan"
L_MONGODB_COLLECTION = "laifu"
P_MONGODB_COLLECTION = "pengfu"
Q_MONGODB_COLLECTION = "qiubai"


USER_AGENT = 'Mozilla/6.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

