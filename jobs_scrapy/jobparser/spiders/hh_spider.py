import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader


class HhSpider(scrapy.Spider):
    name = 'hh_spider'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=python&showClusters=true']

    def parse(self, response: HtmlResponse):
        next_page = \
            response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy_items = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in vacansy_items:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        # title = response.xpath("//h1[@data-qa='vacancy-title']/span/text()").extract_first()
        # salary_from = \
        #     response.xpath("//span[@itemprop='baseSalary']//meta[@itemprop='minValue']/@content").extract_first()
        # salary_till = \
        #     response.xpath("//span[@itemprop='baseSalary']//meta[@itemprop='maxValue']/@content").extract_first()
        # currency = response.xpath("//span[@itemprop='baseSalary']//meta[@itemprop='currency']/@content").extract_first()
        # link = response.xpath("//meta[@itemprop='url']/@content").extract_first()
        # yield JobparserItem(title=title, salary_from=salary_from, salary_till=salary_till, currency=currency, link=link)
        loader = ItemLoader(item=JobparserItem(), response=response)

        # loader.add_xpath('price', '(//span[@class="js-item-price"])[1]/@content')
        loader.add_xpath('title', "//h1[@data-qa='vacancy-title']/span/text()")
        loader.add_xpath('salary_from', "//span[@itemprop='baseSalary']//meta[@itemprop='minValue']/@content")
        loader.add_xpath('salary_till', "//span[@itemprop='baseSalary']//meta[@itemprop='maxValue']/@content")
        loader.add_xpath('currency', "//span[@itemprop='baseSalary']//meta[@itemprop='currency']/@content")
        loader.add_xpath('link', "//meta[@itemprop='url']/@content")


        yield loader.load_item()
