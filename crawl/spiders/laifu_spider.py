import os
import json
import scrapy

from crawl.items import JokeItem


class JokeSpider(scrapy.Spider):
    name = "laifu"
    allowed_domains = ["http://www.laifudao.com/"]
    url_list = []
    for i in range(1, 11):
        page_url = "http://www.laifudao.com/wangwen/lengxiaohua_%s.htm" % str(i)
        url_list.append(page_url)
    start_urls = url_list

    def parse(self, response):
        sites = response.xpath('//article[re:test(@id, "post-id-\d{6}")]')
        items = []
        for site in sites:
            sub_site = site.xpath('div[@class="post-content stickem-container"]')
            item = JokeItem()
            item['id'] = site.xpath('@data-post-id').extract()
            item['content'] = sub_site.xpath('section[@class="article-content"]/p/text()').extract()
            item['via_url'] = unicode('http://www.laifudao.com/') + \
                              site.xpath('header[@class="post-header"]/h1/a/@href').extract()[0]
            item['via'] = unicode('laifudao')
            items.append(item)

        return items
