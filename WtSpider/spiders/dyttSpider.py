# -*- coding: utf-8 -*-
import scrapy

from WtSpider.items import DyttspiderItem


class DyttSpider(scrapy.Spider):
    name = 'dytt'
    allowed_domains = ['www.ygdy8.net']

    url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_'
    offset = 1

    start_urls = [url + str(offset) + '.html']

    def parse(self, response):

        items = []
        for each in response.xpath('//table[@class="tbspan"]'):
            item = DyttspiderItem()
            title = each.xpath('.//a/text()').extract()
            data = each.xpath('.//font/text()').extract()
            intro = each.xpath('./tr[4]/td/text()').extract()
            url = each.xpath('.//a/@href').extract()
            if title:
                item['title'] = title[0]
            else:
                item['title'] = '暂无数据'
            if data:
                item['data'] = data[0]
            else:
                item['data'] = '暂无数据'
            if intro:
                item['intro'] = intro[0]
            else:
                item['intro'] = '暂无数据'
            if url:
                item['url'] = 'http://www.ygdy8.net' + url[0]
            else:
                item['url'] = '暂无数据'
            items.append(item)

        for item in items:
            yield scrapy.Request(url=item['url'], meta={'meta': item}, callback=self.detail_parse)

        for count in response.xpath('//div[@class="co_content8"]/div[@class="x"]'):
            countNum = count.xpath('.//a/text()').extract()
            for a in countNum:
                if '下一页' in a:
                    self.offset += 1

        yield scrapy.Request(self.url + str(self.offset) + '.html', callback=self.parse)

    def detail_parse(self, response):
        item = response.meta['meta']
        # content = ''
        # content_list = response.xpath('//div[@id="Zoom"]//p/text()').extract()
        # # 将p标签里的文本内容合并到一起
        # for content_one in content_list:
        #     content += content_one
        #
        # item['content'] = content
        downloadUrl = response.xpath('//div[@id="Zoom"]//a/text()').extract()
        if downloadUrl:
            item['downloadUrl'] = downloadUrl[0]
        else:
            item['downloadUrl'] = '暂无下载链接'
        yield item
