from scrapy import cmdline
import time
import os

min = [
    'scrapy crawl testSpider',
    'scrapy crawl sinaSpider',
    'scrapy crawl dyttSpider',
    'scrapy crawl scggzySpider',
    'scrapy crawl jokeSpider',
    'scrapy crawl zakerSpider',
]
# cmdline.execute(min[3].split())


# 定时任务
while True:
    print('开始执行>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    os.system(min[3])
    time.sleep(86400)  # 每隔一天运行一次 24*60*60=86400s
