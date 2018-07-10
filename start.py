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
cmdline.execute(min[3].split())


# 定时任务
# while True:
#     print('开始执行>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
#     os.system(min[3])
#     time.sleep(3600)  # 每隔两小时运行一次 2*60*60=86400s
