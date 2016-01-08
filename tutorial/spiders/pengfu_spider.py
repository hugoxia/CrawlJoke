import os
import json
import scrapy

from tutorial.items import JokeItem


class JokeSpider(scrapy.Spider):
    name = "pengfu"
    allowed_domains = ["pengfu.com"]
    start_urls = ["http://www.pengfu.com/xiaohua_1.html"]

    def parse(self, response, name='pengfu'):
        # sel = scrapy.selector.Selector(response)
        sites = response.xpath('//div[@class="tieziBox"]')
        items = []
        for site in sites:
            sub_site = site.xpath('div[@class="contFont"]')
            item = JokeItem()
            item['title'] = sub_site.xpath('div[@class="tieTitle"]/a[@href]/text()').extract()
            item['content'] = sub_site.xpath(
                'div[@class="imgbox"]/div[@class="humordatacontent  imgboxBtn"]/text()').extract()
            item['via_url'] = sub_site.xpath('div[@class="tieTitle"]/a[@href]').extract()
            item['via'] = unicode('pengfuwang')
            items.append(item)

        return save_joke(filename=name, content=items)


def save_joke(folder='collection', filename=None, content=None):
    try:
        os.chdir('../')
        os.mkdir(folder)
    except OSError as e:
        print(e)
    finally:
        os.chdir(folder)

    with open(filename+'.json', 'w') as f:
        jokes_dict = {'jokes': content}
        print(jokes_dict)
        json.dump(jokes_dict, f)
