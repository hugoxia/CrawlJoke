import scrapy
 
from crawl.items import JokeItem


class JokeSpider(scrapy.Spider):
    name = "joke"
    allowed_domains = ["qiushibaike.com"]
    url_list = []
    for i in range(1, 11):
        page_url = "http://www.qiushibaike.com/8hr/page/" + str(i)
        url_list.append(page_url)
    start_urls = url_list
 
    def parse(self, response):
        # sel = scrapy.selector.Selector(response)
        sites = response.xpath('//div[@class="article block untagged mb15"]')
        items = []
        for site in sites:
            url = site.xpath('div[@class="author clearfix"]/a[@rel="nofollow"]/@href')
            if len(url) != 0:
                item = JokeItem()
                item['content'] = site.xpath('div[@class="content"]/text()').extract()[0]
                item['via_url'] = unicode("http://www.qiushibaike.com") + \
                    site.xpath('div[@class="author clearfix"]/a[@rel="nofollow"]/@href').extract()[0]
                item['via'] = unicode('qiushibaike')
                items.append(item)

        return items
