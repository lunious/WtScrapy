# -*- coding: utf-8 -*-
import datetime
import json
import time
import scrapy
from WtSpider.items import ScggjyItem


class ScggzyspiderSpider(scrapy.Spider):
    name = 'scggzySpider'
    allowed_domains = ['scggzy.gov.cn']
    page = 1
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 转换成时间数组
    timeArray = time.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = int(time.mktime(timeArray))
    url = 'http://www.scggzy.gov.cn/Info/GetInfoListNew?keywords=&times=4&timesStart=&timesEnd=&province=&area=&businessType=&informationType=&industryType='
    start_urls = [url + '&page=' + str(page) + '&parm=' + str(timestamp)]

    def parse(self, response):
        js = json.loads(response.body_as_unicode())
        if '成功' == js['message']:
            data = json.loads(js['data'])
            pageCount = js['pageCount']
            items = []
            for each in data:
                item = ScggjyItem()
                item['sTitle'] = each['Title']
                item['sDetailLink'] = 'http://www.scggzy.gov.cn' + each['Link']
                item['sPubData'] = each['CreateDateStr']
                items.append(item)
            for item in items:
                yield scrapy.Request(url=item['sDetailLink'], meta={'meta': item}, callback=self.detail_parse)

            if self.page < pageCount:
                self.page += 1

            yield scrapy.Request(url=self.url + '&page=' + str(self.page) + '&parm=' + str(self.timestamp))

    def detail_parse(self, response):
        item = response.meta['meta']
        detailTitle = response.xpath('//div[@class="titFontname"]/text()').extract()
        if detailTitle:
            item['sDetailTitle'] = detailTitle[0]
        else:
            item['sDetailTitle'] = item['sTitle']
        yield item
