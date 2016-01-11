import os
import json
import scrapy

from crawl.items import JokeItem


class JokeSpider(scrapy.Spider):
    name = "jandan"
    allowed_domains = ["http://jandan.net/duan"]
    start_urls = ["http://jandan.net/duan"]

    def parse(self, response):
        # get number of a first page address
        index = response.xpath('//span[@class="current-comment-page"]/text()').extract()
        print(index)
        sites = response.xpath('//li[re:test(@id, "comment-\d{7}")]')
        items = []
        for site in sites:
            sub_site = site.xpath('div/div[@class="row"]')
            img = sub_site.xpath('div[@class="text"]/p/img')
            if len(img) == 0:
                item = JokeItem()
                item['id'] = sub_site.xpath('div[@class="text"]/span[@class="righttext"]/a/text()').extract()
                item['content'] = sub_site.xpath('div[@class="text"]/p/text()').extract()
                item['via_url'] = sub_site.xpath('div[@class="text"]/span[@class="righttext"]/a/@href').extract()
                item['via'] = unicode('jandanwang')
                items.append(item)
            else:
                pass

        return items
