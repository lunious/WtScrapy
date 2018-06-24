# -*- coding: utf-8 -*-
import scrapy


class TestspiderSpider(scrapy.Spider):
    name = 'testSpider'
    allowed_domains = ['test.com']
    start_urls = ['http://www.baidu.com']

    def parse(self, response):
        print(response.body)
        pass
