import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader


class AvitoSpider(scrapy.Spider):
    def __init__(self):
        self.main_link = 'https://avito.ru'
        self.cur_page = 1

    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva/knigi_i_zhurnaly/uchebnaya_literatura']

    def parse(self, response: HtmlResponse):
        next_page = f"{self.main_link}/moskva/knigi_i_zhurnaly/uchebnaya_literatura?p={self.cur_page + 1}"
        self.cur_page += 1
        yield response.follow(next_page, callback=self.parse)
        books_links = response.xpath("//div[@data-marker='item']//a/@href").extract()
        for link in books_links:
            yield response.follow(link, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_css('title','h1.title-info-title span.title-info-title-text::text')
        loader.add_xpath('photos','//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_xpath('price', '(//span[@class="js-item-price"])[1]/@content')
        loader.add_xpath('geo', '//span[@class="item-address__string"]/text()')
        loader.add_xpath('description', '//div[@class="item-description-text"]//text()')

        yield loader.load_item()
