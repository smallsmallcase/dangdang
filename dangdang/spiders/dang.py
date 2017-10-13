# -*- coding: utf-8 -*-
import scrapy
# from scrapy import Selector
from dangdang.items import DangdangItem
# from scrapy.http.request import Request
from scrapy import FormRequest  # 最好用这个，功能更全
from scrapy.http import TextResponse


class DangSpider(scrapy.Spider):
    name = 'dang'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://www.dangdang.com']

    def start_requests(self):
        for page in range(100):
            page += 1
            url = 'http://search.dangdang.com/?key=%B1%CA%BC%C7%B1%BE%B5%E7%C4%D4&SearchFromTop=1&catalog=&page_index={}'.format(page)
            # url = 'http://search.dangdang.com/?key=%B1%CA%BC%C7%B1%BE%B5%E7%C4%D4&act=input&att=1%3A1066&page_index={}'.format(page)
            yield FormRequest(url=url, callback=self.parse)

    def parse(self, response):
        # hax = Selector(response)
        items = []
        titles = response.xpath('//body//div[@id="search_nature_rg"]//a/@href').extract()
        for index in range(len(titles)):
            item = DangdangItem()
            title =titles[index]
            item['links'] = title
            items.append(item)
        for item in items:
            yield FormRequest(dont_filter=True, url=item['links'], meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta['item']
        name = response.xpath('//body//h1/@title').extract()
        price = response.xpath('//*[@id="dd-price"]/text()').extract()
        item['name'] = name
        item['price'] = price
        yield item
