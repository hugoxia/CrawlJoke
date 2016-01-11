import os
import re
import json
import scrapy

from scrapy.http import Request
from crawl.items import JokeItem


class JokeSpider(scrapy.Spider):
    name = "fml"
    allowed_domains = ["jandan.net"]
    start_urls = ["http://jandan.net/tag/%E5%8F%91%E9%9C%89%E5%95%A6"]

    def parse(self, response):
        urls = response.xpath('//div[@class="thumbs_b"]/a/@href').extract()
        for url in urls:
            yield Request(str(url), callback=self.parse2)

    def parse2(self, response):
        sites = response.xpath('//div[@class="post f"]/p')
        items = []
        for site in sites:
            if len(site.xpath('text()')) > 1:
                item = JokeItem()
                item['via_url'] = site.xpath('a/@href').extract()
                item['content'] = site.xpath('text()').extract()[-1]
                item['id'] = re.split(r'[/]', str(item["via_url"][0]))[-1]
                items.append(item)
            else:
                pass

        return items

