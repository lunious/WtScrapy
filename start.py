from scrapy import cmdline

min = [
    'scrapy crawl sina', 'scrapy crawl dytt',
]
cmdline.execute(min[1].split())
