# -*- coding: utf-8 -*-
import scrapy


class TestspiderSpider(scrapy.Spider):
    name = 'testSpider'
    allowed_domains = ['test.com']
    start_urls = ['http://xyxxgk.hnsl.gov.cn/Judge.aspx?d=4']

    def start_requests(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        }
        return [scrapy.Request(url=self.start_urls[0], headers=self.header, callback=self.parse, dont_filter=True)]

    def parse(self, response):
        state = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract()[0]
        tion = response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract()[0]
        aa = response.xpath('//*[@id="ContentPlaceHolder1_GridViewJudge_LabelPageCount"]/text()').extract()[0]
        print(aa)

        count = 0
        while count < 40:
            s = '//*[@id="ContentPlaceHolder1_GridViewJudge_HyperLink1_' + str(count) + '\"' + ']' + '/text()'
            item = response.xpath(s).extract()[0]
            print(item)
            count += 1

        data = {
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$GridViewJudge$ctl43$LinkButtonNextPage',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': state,
            '__EVENTVALIDATION': tion,
            'ctl00$ContentPlaceHolder1$ddlYEAR': '0',
            'ctl00$ContentPlaceHolder1$TextBoxName': '',
            'ctl00$ContentPlaceHolder1$ddlJINDE': '0',
            'ctl00$ContentPlaceHolder1$ddlRESULT/': '全部',
            '/ctl00$ContentPlaceHolder1$GridViewJudge$ctl43$txtNewPageIndex': '1',
        }

        yield scrapy.FormRequest(url=self.start_urls[0], callback=self.post_parse, headers=self.header,
                                 formdata=data,
                                 dont_filter=True)

    def post_parse(self, response):
        state = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract()[0]
        tion = response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract()[0]

        limit_size = response.xpath('//*[@id="ContentPlaceHolder1_GridViewJudge"]/tbody/tr').extract()
        print(limit_size)

        count = 0
        while count < 40:
            s = '//*[@id="ContentPlaceHolder1_GridViewJudge_HyperLink1_' + str(count) + '\"' + ']' + '/text()'
            item = response.xpath(s).extract()[0]
            print(item)
            count += 1

        data = {
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$GridViewJudge$ctl43$LinkButtonNextPage',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': state,
            '__EVENTVALIDATION': tion,
            'ctl00$ContentPlaceHolder1$ddlYEAR': '0',
            'ctl00$ContentPlaceHolder1$TextBoxName': '',
            'ctl00$ContentPlaceHolder1$ddlJINDE': '0',
            'ctl00$ContentPlaceHolder1$ddlRESULT/': '全部',
            '/ctl00$ContentPlaceHolder1$GridViewJudge$ctl43$txtNewPageIndex': '1',
        }

        yield scrapy.FormRequest(url=self.start_urls[0], callback=self.post_parse, headers=self.header,
                                 formdata=data,
                                 dont_filter=True)
