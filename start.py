from scrapy import cmdline

min = [
    'scrapy crawl testSpider',
    'scrapy crawl sinaSpider',
    'scrapy crawl dyttSpider',
    'scrapy crawl scggzySpider',
    'scrapy crawl jokeSpider',

]
cmdline.execute(min[0].split())
