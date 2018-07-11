# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
import pymysql
from wscrapy import settings
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename, dirname, join


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


# 全国公共交易网（四川）
class ScggjyPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            port=settings.MYSQL_PORT,
            charset='utf8',
            use_unicode=False
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        if item['entryOwner'] != '':
            try:
                self.cursor.execute(
                    "insert into sggjyzbjg (reportTitle,sysTime,url,entryName,entryOwner,ownerTel,tenderee,tendereeTel,biddingAgency,biddingAgencTel,placeAddress,placeTime,publicityPeriod,bigPrice,oneTree,twoTree,threeTree,treeCount) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE reportTitle = reportTitle",
                    (item['reportTitle'],
                     item['sysTime'],
                     item['url'],
                     item['entryName'],
                     item['entryOwner'],
                     item['ownerTel'],
                     item['tenderee'],
                     item['tendereeTel'],
                     item['biddingAgency'],
                     item['biddingAgencTel'],
                     item['placeAddress'],
                     item['placeTime'],
                     item['publicityPeriod'],
                     item['bigPrice'],
                     item['oneTree'],
                     item['twoTree'],
                     item['threeTree'],
                     item['treeCount'],
                     ))
                self.connect.commit()
            except Exception as error:
                logging.log(error)
            try:
                self.cursor.execute("Insert into entryjglist(entryName,sysTime,type,entity,entityId) select reportTitle,sysTime,'工程中标结果','sggjyzbjg',id from sggjyzbjg where id not in(select entityId from entryjglist where  entity ='sggjyzbjg' ) ")
                self.connect.commit()
            except Exception as error:
                logging.log(error)
            try:
                self.cursor.execute("update sggjy set sggjyzbjgId=(select id from sggjyzbjg where url =%s )", item['url'])
                self.connect.commit()
            except Exception as error:
                logging.log(error)
            return item

    def close_spider(self, spider):
        self.connect.close()


# 笑话
class JokePipeline(object):
    def process_item(self, item, spider):
        fp = open('./data/' + item['jTitle'] + '.txt', 'wb')
        fp.write(item['jContent'].encode('utf-8'))
        fp.close()

        return item


# zaker新闻
class ZakerPipeline(object):

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
                "INSERT INTO zaker_news (zTitle, zSubtitle, sSubImageLink,zDetailLink,zType,zInsertData) VALUES(%s, %s, %s,%s,%s,%s) ON DUPLICATE KEY UPDATE zSubtitle = zSubtitle",
                (item['zTitle'],
                 item['zSubtitle'],
                 item['sSubImageLink'],
                 item['zDetailLink'],
                 item['zType'],
                 item['zInsertData'],
                 ))
            self.connect.commit()
        except Exception as error:
            logging.log(error)
        return item

    def close_spider(self, spider):
        self.connect.close()


# Matplotlib
class MatplotlibPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        return join(basename(dirname(path)), basename(path))
