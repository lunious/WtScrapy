from scrapy import cmdline

min = [
    'scrapy crawl test', 'scrapy crawl sina', 'scrapy crawl dytt',
]
cmdline.execute(min[2].split())
