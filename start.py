from scrapy import cmdline

min = [
    'scrapy crawl testSpider', 'scrapy crawl sinaspider', 'scrapy crawl dyttspider', 'scrapy crawl scggzySpider',
]
cmdline.execute(min[3].split())
