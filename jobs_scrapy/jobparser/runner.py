from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser import settings
from jobparser.spiders.hh_spider import HhSpider
from jobparser.spiders.superjob_spider import SuperjobSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhSpider)
    process.crawl(SuperjobSpider)
    process.start()
