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
                item['id'] = str(
                    sub_site.xpath('div[@class="imgbox"]/div[@class="humordatacontent  imgboxBtn"]/id')[0])
            except IndexError:
                item['id'] = None
            try:
                item['title'] = str(
                    sub_site.xpath('div[@class="tieTitle"]/a[@href]/text()').extract()[0])
            except IndexError:
                item['title'] = None
            try:
                item['content'] = str(sub_site.xpath(
                'div[@class="imgbox"]/div[@class="humordatacontent  imgboxBtn"]/text()').extract()[0])
            except IndexError:
                item['content'] = None
            try:
                item['via_url'] = str(sub_site.xpath('div[@class="tieTitle"]/a/@href').extract()[0])
            except IndexError:
                item['via_url'] = None
            item['via'] = 'pengfuwang'
            items.append(item)

        return items

#         return save_joke(filename=name, content=items)
#
#
# def save_joke(folder='collection', filename=None, content=None):
#     try:
#         os.chdir('../')
#         os.mkdir(folder)
#     except OSError as e:
#         print(e)
#     finally:
#         os.chdir(folder)
#
#     with open(filename+'.json', 'w') as f:
#         jokes_dict = {'jokes': content}
#         print(jokes_dict)
#         json.dump(jokes_dict, f)
