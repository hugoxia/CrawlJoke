import scrapy

from crawl.items import JokeItem


class JokeSpider(scrapy.Spider):
    name = "qiubai"
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
                try:
                    item['id'] = site.xpath('@id').re('\d{1,15}')[0]
                except IndexError:
                    item['id'] = None
                try:
                    item['content'] = ''.join(site.xpath('div[@class="content"]//text()').extract()).replace('\n', '')
                except IndexError:
                    item['content'] = None
                try:
                    item['via_url'] = "http://www.qiushibaike.com" + \
                                      site.xpath('div[@class="author clearfix"]/a[@rel="nofollow"]/@href').extract()[0]
                except IndexError:
                    item['via_url'] = None
                item['via'] = 'qiubai'
                items.append(item)
            else:
                pass

        return items
