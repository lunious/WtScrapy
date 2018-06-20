import os

import scrapy

from WtSpider.items import SinaItem


class SinaSpider(scrapy.Spider):
    name = 'sinaSpider'
    allowed_domain = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        items = []
        # 所有大类的url和标题
        parentUrls = response.xpath('//div[@id=\"tab01\"]/div/h3/a/@href').extract()
        parentTitles = response.xpath('//div[@id=\"tab01\"]/div/h3/a/text()').extract()

        # 所有小类的url和标题
        subUrls = response.xpath('//div[@id=\"tab01\"]/div/ul/li/a/@href').extract()
        subTitles = response.xpath('//div[@id=\"tab01\"]/div/ul/li/a/text()').extract()

        # 爬取所有大类
        for i in range(0, len(parentTitles)):
            # 指定大类目录的路径和目录名
            parentFilename = './Data/' + parentTitles[i]

            # 如果目录不存在，则拆创建目录
            if (not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)

            # 爬取所有小类
            for j in range(0, len(subTitles)):
                item = SinaItem()

                # 保存大类的title和urls
                item['parentTitle'] = parentTitles[i]
                item['parentUrl'] = parentUrls[i]

                # 检查小类的Url是否以同类别大类的url开头，如果是返回true(sports.sina.com.cn和sports)
                if_belong = subUrls[j].startswith(item['parentUrl'])

                # 如果属于本大类，将存储目录放在本大类目录下
                if (if_belong):
                    subFilename = parentFilename + '/' + subTitles[j]
                    # 如果目录不存在，则创建目录
                    if (not os.path.exists(subFilename)):
                        os.makedirs(subFilename)

                    # 存储小类的url、title和filename字段数据
                    item['subUrl'] = subUrls[j]
                    item['subTitle'] = subTitles[j]
                    item['subFilename'] = subFilename

                    items.append(item)

        # 发送每个小类url的Request请求，得到Response连同包含meta数据一同返交给回调函数second_pares方法
        for item in items:
            yield scrapy.Request(url=item['subUrl'], meta={'meta_1': item}, callback=self.second_parse)

    # 对于返回的小类url，再进行递归请求
    def second_parse(self, response):
        # 提取每次Response的meta数据
        meta_1 = response.meta['meta_1']

        # 提取出小类里的所有子链接
        sonUrls = response.xpath('//a/@href').extract()

        items = []
        for i in range(0, len(sonUrls)):
            # 检查每个链接是否以大类url开头，以.shtml结尾，如果是返回true
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(meta_1['parentUrl'])

            # 如果属于本大类，获取字段值放在同一个item下便于传输
            if (if_belong):
                item = SinaItem()
                item['parentTitle'] = meta_1['parentTitle']
                item['parentUrl'] = meta_1['parentUrl']
                item['subUrl'] = meta_1['subUrl']
                item['subTitle'] = meta_1['subTitle']
                item['subFilename'] = meta_1['subFilename']
                item['sonUrl'] = sonUrls[i]

                items.append(item)

        # 发送每个小类下子链接url的Response请求，得到Response后连同包含Metas数据一同交给回调函数detail_parse
        for item in items:
            yield scrapy.Request(url=item['sonUrl'], meta={'meta_2': item}, callback=self.detail_parse)

    def detail_parse(self, response):
        # 提取每次Response的meta数据
        item = response.meta['meta_2']
        content = ''
        head = response.xpath('//html/body/div[3]/h1/text()').extract()
        content_list = response.xpath('//div[@id=\"artibody\"]/p/text()').extract()

        # 将p标签里的文本内容合并到一起
        for content_one in content_list:
            content += content_one

        item['head'] = head
        item['content'] = content

        yield item
