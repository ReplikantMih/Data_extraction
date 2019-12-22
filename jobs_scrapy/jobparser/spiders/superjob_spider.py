import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import json
from scrapy.loader import ItemLoader


class SuperjobSpider(scrapy.Spider):
    name = 'superjob_spider'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy_items = response.xpath("//div[contains(@class, 'vacancy-item')]//a[@target='_blank']/@href").extract()
        for link in vacansy_items:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        # title = response.xpath("//div[@id='app']//h1/text()").extract_first()
        base_salary = json.loads(response.xpath("//script[@type='application/ld+json']/text()").extract()[1]).get('baseSalary', None)
        if not base_salary:
            base_salary = {'value': {'minValue': None, 'maxValue': None}, 'currency': None}
        salary_from = base_salary['value'].get('minValue', None)
        salary_till = base_salary['value'].get('maxValue', None)
        currency = base_salary.get('currency', None)
        # link = json.loads(response.xpath("//script[@type='application/ld+json']/text()").extract()[0])['itemListElement'][-1]['item']['@id']
        # yield JobparserItem(title=title, salary_from=salary_from, salary_till=salary_till, currency=currency, link=link)

        # loader.add_xpath('price', '(//span[@class="js-item-price"])[1]/@content')
        loader = ItemLoader(item=JobparserItem(), response=response)


        loader.add_xpath('title', "//div[@id='app']//h1/text()")
        loader.add_value('salary_from', [salary_from])
        loader.add_value('salary_till', [salary_till])
        loader.add_value('currency', [currency])
        loader.add_xpath('link', '(//span[@class="js-item-price"])[1]/@content')




        yield loader.load_item()
