from scrapy import cmdline

min = [
    'scrapy crawl testSpider',
    'scrapy crawl sinaSpider',
    'scrapy crawl dyttSpider',
    'scrapy crawl scggzySpider',
    'scrapy crawl jokeSpider',
    'scrapy crawl zakerSpider',
]
cmdline.execute(min[3].split())
