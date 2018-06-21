from scrapy import cmdline

min = [
    'scrapy crawl testSpider',
    'scrapy crawl sinaSpider',
    'scrapy crawl dyttSpider',
    'scrapy crawl scggzySpider',
    'scrapy crawl jokeSpider',

]
cmdline.execute(min[2].split())
