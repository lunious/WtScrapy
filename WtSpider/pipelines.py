# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


# 电影天堂
class DyttPipeline(object):

    def __init__(self):
        self.filename = open('dytt.json', 'wb')

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.filename.write(text.encode('utf-8'))
        return item

    def close_spider(self, spider):
        self.filename.close()


# 新浪新闻
class SinaPipeline(object):
    def process_item(self, item, spider):
        sonUrl = item['sonUrl']

        # 将文件名为子链接url中间部分，并将/替换为_,保存为.txt格式
        filename = sonUrl[7:-6].replace('/', '_')
        filename += '.txt'

        fp = open(item['subFilename'] + '/' + filename, 'wb')
        fp.write(item['content'].encode('utf-8'))
        fp.close()

        return item
