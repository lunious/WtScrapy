from scrapy import cmdline

min = [
    'scrapy crawl testSpider',
    'scrapy crawl sinaspider',
    'scrapy crawl dyttspider',
    'scrapy crawl scggzySpider',
    'scrapy crawl jokeSpider',

]
cmdline.execute(min[4].split())
