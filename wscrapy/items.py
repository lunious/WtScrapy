# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WtscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 电影天堂
class DyttspiderItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    data = scrapy.Field()  # 日期
    intro = scrapy.Field()  # 简介
    url = scrapy.Field()  # 详情连接
    # content = scrapy.Field()  # 详情
    downloadUrl = scrapy.Field()  # 下载链接


# 新浪新闻
class SinaItem(scrapy.Item):
    # 大类的标题和url
    parentTitle = scrapy.Field()
    parentUrl = scrapy.Field()

    # 小类的标题和子url
    subTitle = scrapy.Field()
    subUrl = scrapy.Field()

    # 小类目录存储路径
    subFilename = scrapy.Field()

    # 小类下的子链接
    sonUrl = scrapy.Field()

    # 文章标题和内容
    head = scrapy.Field()
    content = scrapy.Field()


# 全国公共交易平台
class ScggjyItem(scrapy.Item):
    sTitle = scrapy.Field()
    sDetailLink = scrapy.Field()
    sPubData = scrapy.Field()
    sDetailTitle = scrapy.Field()


# 笑话
class JokeItem(scrapy.Item):
    jTitle = scrapy.Field()
    jDetailLink = scrapy.Field()
    jContent = scrapy.Field()


# zaker
class ZakerItem(scrapy.Item):
    zTitle = scrapy.Field()
    zSubtitle = scrapy.Field()
    sSubImageLink = scrapy.Field()
    zDetailLink = scrapy.Field()
    zType = scrapy.Field()
