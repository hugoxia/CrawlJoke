import os
import json
import scrapy

from crawl.items import JokeItem


class JokeSpider(scrapy.Spider):
    name = "pengfu"
    allowed_domains = ["pengfu.com"]
    start_urls = ["http://www.pengfu.com/xiaohua_%s.html" % i for i in range(1, 11)]

    def parse(self, response, name='pengfu'):
        # sel = scrapy.selector.Selector(response)
        sites = response.xpath('//div[@class="tieziBox"]')
        items = []
        for site in sites:
            sub_site = site.xpath('div[@class="contFont"]')
            item = JokeItem()
            try:
                item['id'] = sub_site.xpath('div[@class="imgbox"]\
                /div[@class="humordatacontent  imgboxBtn"]/@id').re('\d{1,15}')[0]
            except IndexError:
                item['id'] = None
            try:
                item['title'] = sub_site.xpath('div[@class="tieTitle"]\
                /a[@href]/text()').extract()[0]
            except IndexError:
                item['title'] = None
            try:
                item['content'] = sub_site.xpath('div[@class="imgbox"]\
                /div[@class="humordatacontent  imgboxBtn"]/text()').extract()[0].replace('\n', '')
            except IndexError:
                item['content'] = None
            try:
                item['via_url'] = sub_site.xpath('div[@class="tieTitle"]\
                /a/@href').extract()[0]
            except IndexError:
                item['via_url'] = None
            item['via'] = 'pengfu'
            items.append(item)

        return items
