# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

# 电影天堂
import logging

import pymysql

from wscrapy import settings


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


# 全国公共交易网（四川）
class ScggjyPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                "insert into scggjy (title, pubData, detailLink,detailTitle) value(%s, %s, %s,%s)",
                (item['sTitle'],
                 item['sPubData'],
                 item['sDetailLink'],
                 item['sDetailTitle'],
                 ))
            self.connect.commit()
        except Exception as error:
            logging.log(error)
        return item

    def close_spider(self, spider):
        self.connect.close()


# 笑话
class JokePipeline(object):
    def process_item(self, item, spider):

        fp = open('./data/'+item['jTitle'] + '.txt', 'wb')
        fp.write(item['jContent'].encode('utf-8'))
        fp.close()

        return item
