# -*- coding: utf-8 -*-
import json
import scrapy
from wscrapy.items import ZakerItem
import datetime

class ZakerspiderSpider(scrapy.Spider):
    name = 'zakerSpider'
    allowed_domains = ['www.myzaker.com']

    typeDic = {'660': '热点', '9': '娱乐', '7': '汽车', '8': '体育', '13': '科技', '1': '国内', '2': '国际', '3': '军事', '4': '汽财经',
               '5': '互联网',
               '11': '教育', '12': '时尚', '1014': '星座', '959': '亲子', '14': '社会', '981': '旅游', '1039': '科学', '10820': '健康',
               '11195': '理财', '1067': '奢侈品',
               '10386': '美食', '10376': '游戏', '10530': '电影', }

    def start_requests(self):

        baseUrl = 'http://www.myzaker.com/channel/'

        for key in self.typeDic.keys():
            yield scrapy.Request(url=baseUrl + key, meta={'meta': self.typeDic.get(key)}, callback=self.parse)

    def parse(self, response):
        type = response.meta['meta']
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
            item['zType'] = type
            item['zInsertData'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item
        nextUrl = response.xpath('//*[@id="nexturl"]/@value').extract()[0][2:]
        yield scrapy.Request(url='http://' + nextUrl, meta={'meta': type}, callback=self.second_parse)

    def second_parse(self, response):
        type = response.meta['meta']
        js = json.loads(response.body_as_unicode())
        data = js['data']
        article = data['article']
        for each in article:
            item = ZakerItem()
            item['zTitle'] = each['title']
            if 'marks' in each.keys():
                item['zSubtitle'] = each['marks'][0]
            else:
                item['zSubtitle'] = ''
            if 'img' in each.keys():
                item['sSubImageLink'] = each['img'][2:]
            else:
                item['sSubImageLink'] = ''
            item['zDetailLink'] = each['href'][2:-1]
            item['zType'] = type
            item['zInsertData'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item

        # 判断有无下一页
        # if data.has_key('next_url'):
        if 'next_url' in data.keys():
            nextUrl = data['next_url'][2:]
            yield scrapy.Request(url='http://' + nextUrl, meta={'meta': type}, callback=self.second_parse)
            print(nextUrl)
