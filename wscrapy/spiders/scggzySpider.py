# -*- coding: utf-8 -*-
import datetime
import json
import time
import scrapy
from wscrapy.items import ScggjyItem


class ScggzyspiderSpider(scrapy.Spider):
    name = 'scggzySpider'
    # allowed_domains = ['scggzy.gov.cn']
    page = 1
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 转换成时间数组
    timeArray = time.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = int(time.mktime(timeArray))
    url = 'http://www.scggzy.gov.cn/Info/GetInfoListNew?keywords=&times=5&timesStart=&timesEnd=&province=&area=&businessType=project&informationType=TenderCandidateAnnounce&industryType='
    start_urls = [url + '&page=' + str(page) + '&parm=' + str(timestamp)]

    def parse(self, response):
        js = json.loads(response.body_as_unicode())
        if '成功' == js['message']:
            data = json.loads(js['data'])
            pageCount = js['pageCount']
            items = []
            for each in data:
                item = ScggjyItem()
                item['reportTitle'] = each['Title']
                item['sysTime'] = each['CreateDateStr']
                item['url'] = 'http://www.scggzy.gov.cn' + each['Link']
                items.append(item)
            for item in items:
                yield scrapy.Request(url=item['url'], meta={'meta': item}, callback=self.get_detailLink)

            # if self.page < pageCount:
            #     self.page += 1
            #
            # yield scrapy.Request(url=self.url + '&page=' + str(self.page) + '&parm=' + str(self.timestamp))

    def get_detailLink(self, response):
        meta = response.meta['meta']
        ywLink = response.xpath('//div[@class="ContentMiddle"]//div[@class="deMidd_Nei"]/div[6]//div[@class="deMNei_date"]/a/@href').extract()[0]
        print(ywLink)
        yield scrapy.Request(url=ywLink, meta={'meta': meta}, callback=self.detail_parse)

    def detail_parse(self, response):
        item = response.meta['meta']
        entryName = response.xpath('//*[@id="Label_SECTIONNAME2"]/text()')
        entryOwner = response.xpath('//*[@id="Label_OWNERNAME"]/text()')
        if entryName:
            item['entryName'] = entryName.extract()[0]
        else:
            item['entryName'] = item['reportTitle']
        if entryOwner:
            item['entryOwner'] = entryOwner.extract()[0]
        else:
            item['entryOwner'] = ''
        yield item
