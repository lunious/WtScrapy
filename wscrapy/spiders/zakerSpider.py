# -*- coding: utf-8 -*-
import json

import scrapy
from wscrapy.items import ZakerItem


class ZakerspiderSpider(scrapy.Spider):
    name = 'zakerSpider'
    allowed_domains = ['www.myzaker.com']

    start_urls = ['http://www.myzaker.com/channel/660', ]

    def parse(self, response):
        for each in response.xpath('//*[@id="section"]/div[@class="figure flex-block"]'):
            item = ZakerItem()
            item['zTitle'] = each.xpath('./div[@class="article flex-1"]/h2/a/@title').extract()[0]
            item['zSubtitle'] = each.xpath('./div[@class="article flex-1"]/div/span[1]/text()').extract()[0]
            imageLink = each.xpath('./a/@style').extract()
            if imageLink:
                item['sSubImageLink'] = imageLink[0][23:-2]
            else:
                item['sSubImageLink'] = ''
            item['zDetailLink'] = each.xpath('./div[@class="article flex-1"]/h2/a/@href').extract()[0][2:-1]
            item['zType'] = '热点'
            yield item
        nextUrl = response.xpath('//*[@id="nexturl"]/@value').extract()[0][2:]
        yield scrapy.Request(url='http://' + nextUrl, callback=self.second_parse)

    def second_parse(self, response):
        js = json.loads(response.body_as_unicode())
        data = js['data']
        article = data['article']
        for each in article:
            item = ZakerItem()
            item['zTitle'] = each['title']
            item['zSubtitle'] = each['marks'][0]
            img = each['img']
            if img:
                item['sSubImageLink'] = img[2:]
            else:
                item['sSubImageLink'] = 'null'
            item['zDetailLink'] = each['href'][2:-1]
            item['zType'] = '热点'
            yield item

        # 判断有无下一页
        # if data.has_key('next_url'):
        if 'next_url' in data.keys():
            nextUrl = data['next_url'][2:]
            yield scrapy.Request(url='http://' + nextUrl, callback=self.second_parse)
            print(nextUrl)
