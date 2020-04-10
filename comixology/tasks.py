from comixology import spiders
from scrapy import crawler


def parse_sales():
    process = crawler.CrawlerProcess(
        {"USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"}
    )

    process.crawl(spiders.SalesSpider)
    process.start()


def parse_sales_wishlist():
    process = crawler.CrawlerProcess(
        {"USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"}
    )

    process.crawl(spiders.WishlistComicSpider)
    process.start()
