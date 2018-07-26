# -*- coding: utf-8 -*-
import datetime
import json
import time
import scrapy
from wscrapy.items import ScggjyItem
from scrapy.selector import Selector


class ScggzyspiderSpider(scrapy.Spider):
    name = 'scggzySpider'
    # allowed_domains = ['scggzy.gov.cn']
    page = 1
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 转换成时间数组
    timeArray = time.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = int(time.mktime(timeArray))
    url = 'http://www.scggzy.gov.cn/Info/GetInfoListNew?keywords=&times=2&timesStart=&timesEnd=&province=&area=&businessType=project&informationType=TenderCandidateAnnounce&industryType='
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
                yield scrapy.Request(url=item['url'], meta={'meta': item}, callback=self.detail_parse)

            if self.page < pageCount:
                self.page += 1

            yield scrapy.Request(url=self.url + '&page=' + str(self.page) + '&parm=' + str(self.timestamp))

    def detail_parse(self, response):
        item = response.meta['meta']
        res = response.xpath('//*[@id="hidSeven0"]/@value').extract()
        entryName = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[1]/td[2]/text()').extract()
        entryOwner = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[2]/td[2]/text()').extract()
        ownerTel = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[2]/td[4]/text()').extract()
        tenderee = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[3]/td[2]/text()').extract()
        tendereeTel = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[3]/td[4]/text()').extract()
        biddingAgency = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[4]/td[2]/text()').extract()
        biddingAgencTel = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[4]/td[4]/text()').extract()
        placeAddress = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[5]/td[2]/text()').extract()
        placeTime = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[5]/td[4]/text()').extract()
        publicityPeriod = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[6]/td[2]/text()').extract()
        bigPrice = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[6]/td[4]/text()').extract()
        if entryName:
            item['entryName'] = entryName[0]
        else:
            item['entryName'] = ''
        if entryOwner:
            item['entryOwner'] = entryOwner[0]
        else:
            item['entryOwner'] = ''
        if ownerTel:
            item['ownerTel'] = ownerTel[0]
        else:
            item['ownerTel'] = ''
        if tenderee:
            item['tenderee'] = tenderee[0]
        else:
            item['tenderee'] = ''
        if tendereeTel:
            item['tendereeTel'] = tendereeTel[0]
        else:
            item['tendereeTel'] = ''
        if biddingAgency:
            item['biddingAgency'] = biddingAgency[0]
        else:
            item['biddingAgency'] = ''
        if biddingAgencTel:
            item['biddingAgencTel'] = biddingAgencTel[0]
        else:
            item['biddingAgencTel'] = ''
        if placeAddress:
            item['placeAddress'] = placeAddress[0]
        else:
            item['placeAddress'] = ''
        if placeTime:
            item['placeTime'] = placeTime[0]
        else:
            item['placeTime'] = ''
        if publicityPeriod:
            item['publicityPeriod'] = publicityPeriod[0]
        else:
            item['publicityPeriod'] = ''
        if bigPrice:
            item['bigPrice'] = bigPrice[0]
        else:
            item['bigPrice'] = ''

        ltr = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr').extract()
        if len(ltr) == 4:
            td = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td').extract()
            th = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th').extract()
            if len(th) == 1 and len(td) == 4:
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[1]/text()').extract():
                    o1 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[1]/text()').extract()[0]
                else:
                    o1 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[2]/text()').extract():
                    o2 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[2]/text()').extract()[0]
                else:
                    o2 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[3]/text()').extract():
                    o3 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[3]/text()').extract()[0]
                else:
                    o3 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[4]/text()').extract():
                    o4 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[4]/text()').extract()[0]
                else:
                    o4 = '无'
                item['oneTree'] = o1.strip()+'_'+o2.strip()+'_'+o3.strip()+'_'+o4.strip()
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[1]/text()').extract():
                    t1 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[1]/text()').extract()[0]
                else:
                    t1 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[2]/text()').extract():
                    t2 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[2]/text()').extract()[0]
                else:
                    t2 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[3]/text()').extract():
                    t3 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[3]/text()').extract()[0]
                else:
                    t3 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[4]/text()').extract():
                    t4 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[4]/text()').extract()[0]
                else:
                    t4 = '无'
                item['twoTree'] = t1.strip() + '_' + t2.strip() + '_' + t3.strip() + '_' + t4.strip()
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[1]/text()'):
                    h1 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[1]/text()').extract()[0]
                else:
                    h1 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[2]/text()').extract():
                    h2 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[2]/text()').extract()[0]
                else:
                    h2 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[3]/text()').extract():
                    h3 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[3]/text()').extract()[0]
                else:
                    h3 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[4]/text()').extract():
                    h4 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[4]/text()').extract()[0]
                else:
                    h4 = '无'
                item['threeTree'] = h1.strip() + '_' + h2.strip() + '_' + h3.strip() + '_' + h4.strip()
            elif len(th) == 4 and len(td) == 1:
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[1]/text()').extract():
                    o1 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[1]/text()').extract()[0]
                else:
                    o1 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[2]/text()').extract():
                    o2 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[2]/text()').extract()[0]
                else:
                    o2 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[3]/text()').extract():
                    o3 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[3]/text()').extract()[0]
                else:
                    o3 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[4]/text()').extract():
                    o4 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[4]/text()').extract()[0]
                else:
                    o4 = '无'
                item['oneTree'] = o1.strip()+'_'+o2.strip()+'_'+o3.strip()+'_'+o4.strip()
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[1]/text()').extract():
                    t1 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[1]/text()').extract()[0]
                else:
                    t1 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[2]/text()').extract():
                    t2 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[2]/text()').extract()[0]
                else:
                    t2 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[3]/text()').extract():
                    t3 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[3]/text()').extract()[0]
                else:
                    t3 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[4]/text()').extract():
                    t4 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[4]/text()').extract()[0]
                else:
                    t4 = '无'
                item['twoTree'] = t1.strip() + '_' + t2.strip() + '_' + t3.strip() + '_' + t4.strip()
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[1]/text()'):
                    h1 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[1]/text()').extract()[0]
                else:
                    h1 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[2]/text()').extract():
                    h2 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[2]/text()').extract()[0]
                else:
                    h2 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[3]/text()').extract():
                    h3 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[3]/text()').extract()[0]
                else:
                    h3 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[4]/text()').extract():
                    h4 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[4]/text()').extract()[0]
                else:
                    h4 = '无'
                item['threeTree'] = h1.strip() + '_' + h2.strip() + '_' + h3.strip() + '_' + h4.strip()
            elif len(th) == 0 and len(td) == 5:
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[2]/text()').extract():
                    o1 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[2]/text()').extract()[0]
                else:
                    o1 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[3]/text()').extract():
                    o2 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[3]/text()').extract()[0]
                else:
                    o2 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[4]/text()').extract():
                    o3 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[4]/text()').extract()[0]
                else:
                    o3 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[5]/text()').extract():
                    o4 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[5]/text()').extract()[0]
                else:
                    o4 = '无'
                item['oneTree'] = o1.strip()+'_'+o2.strip()+'_'+o3.strip()+'_'+o4.strip()
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[2]/text()').extract():
                    t1 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[2]/text()').extract()[0]
                else:
                    t1 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[3]/text()').extract():
                    t2 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[3]/text()').extract()[0]
                else:
                    t2 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[4]/text()').extract():
                    t3 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[4]/text()').extract()[0]
                else:
                    t3 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[5]/text()').extract():
                    t4 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[5]/text()').extract()[0]
                else:
                    t4 = '无'
                item['twoTree'] = t1.strip() + '_' + t2.strip() + '_' + t3.strip() + '_' + t4.strip()
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[2]/text()'):
                    h1 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[2]/text()').extract()[0]
                else:
                    h1 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[3]/text()').extract():
                    h2 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[3]/text()').extract()[0]
                else:
                    h2 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[4]/text()').extract():
                    h3 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[4]/text()').extract()[0]
                else:
                    h3 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[5]/text()').extract():
                    h4 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[5]/text()').extract()[0]
                else:
                    h4 = '无'
                item['threeTree'] = h1.strip() + '_' + h2.strip() + '_' + h3.strip() + '_' + h4.strip()
            elif len(th) == 5 and len(td) == 0:
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[2]/text()').extract():
                    o1 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[2]/text()').extract()[0]
                else:
                    o1 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[3]/text()').extract():
                    o2 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[3]/text()').extract()[0]
                else:
                    o2 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[4]/text()').extract():
                    o3 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[4]/text()').extract()[0]
                else:
                    o3 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[5]/text()').extract():
                    o4 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[5]/text()').extract()[0]
                else:
                    o4 = '无'
                item['oneTree'] = o1.strip()+'_'+o2.strip()+'_'+o3.strip()+'_'+o4.strip()
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[2]/text()').extract():
                    t1 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[2]/text()').extract()[0]
                else:
                    t1 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[3]/text()').extract():
                    t2 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[3]/text()').extract()[0]
                else:
                    t2 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[4]/text()').extract():
                    t3 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[4]/text()').extract()[0]
                else:
                    t3 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[5]/text()').extract():
                    t4 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[5]/text()').extract()[0]
                else:
                    t4 = '无'
                item['twoTree'] = t1.strip() + '_' + t2.strip() + '_' + t3.strip() + '_' + t4.strip()
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[2]/text()'):
                    h1 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[2]/text()').extract()[0]
                else:
                    h1 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[3]/text()').extract():
                    h2 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[3]/text()').extract()[0]
                else:
                    h2 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[4]/text()').extract():
                    h3 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[4]/text()').extract()[0]
                else:
                    h3 = '无'
                if Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[5]/text()').extract():
                    h4 = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[5]/text()').extract()[0]
                else:
                    h4 = '无'
                item['threeTree'] = h1.strip() + '_' + h2.strip() + '_' + h3.strip() + '_' + h4.strip()
            else:
                item['oneTree'] = ''
                item['twoTree'] = ''
                item['threeTree'] = ''
                item['entryOwner'] = ''
            if item['oneTree'] or item['twoTree'] or item['threeTree']:
                item['treeCount'] = 3
            else:
                item['treeCount'] = 0

        yield item