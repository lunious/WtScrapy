# -*- coding: utf-8 -*-
import os

import scrapy

from WtSpider.items import JokeItem


class JokespiderSpider(scrapy.Spider):
    name = 'jokeSpider'
    allowed_domains = ['jokeji.cn']
    url = 'http://www.jokeji.cn/list_'
    page = 1
    start_urls = [url + str(page) + '.htm']

    def parse(self, response):
        items = []
        for each in response.xpath('//div[@class = "list_title"]//li'):
            item = JokeItem()
            item['jTitle'] = each.xpath('.//a/text()').extract()[0]
            item['jDetailLink'] = 'http://www.jokeji.cn' + each.xpath('.//a/@href').extract()[0]
            items.append(item)
        for item in items:
            yield scrapy.Request(url=item['jDetailLink'], meta={'meta': item}, callback=self.detail_parse)

        href = response.xpath('//div[@class = "next_page"]//a[text() = "尾页"]/@href').extract()[0]
        print('href==========================================='+href)
        if href.endswith('.htm'):
            self.page += 1
        yield scrapy.Request(self.url + str(self.page) + '.htm', callback=self.parse)

    def detail_parse(self, response):
        item = response.meta['meta']
        content = ''
        content_list = response.xpath('//span[@id="text110"]/p/text()').extract()
        # 将p标签里的文本内容合并到一起
        for content_one in content_list:
            content += content_one
        item['jContent'] = content

        yield item
