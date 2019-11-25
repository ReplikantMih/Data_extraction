import requests
from lxml import html
from time import sleep
from random import randint
from datetime import datetime


class NewsParser:
    def __init__(self, link, source):
        self.avg_seconds_between_attempts = 3
        self.main_link = link
        self.source = source
        self.user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' \
                          r' Chrome/78.0.3904.108 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.html = self.get_html()
        self.DOM = html.fromstring(self.html)
        self.print_started()

    def get_html(self):
        resp = requests.get(url=self.main_link, headers=self.headers)
        return resp.text

    def get_news(self):
        raise NotImplementedError()

    def print_started(self):
        print(f'Parser {self.source} - started...')

    def print_done(self):
        print(f'Parser {self.source} - DONE.')


class MailRuParser(NewsParser):
    def __init__(self):
        super().__init__('https://mail.ru/?from=m', 'mail.ru')

    def get_news(self):
        result_news = []
        news = self.DOM.xpath("//div[@id='news-0']/a")
        for n in news:
            result_n = \
                {'link': n.xpath("./@href")[0].split('?')[0],
                 'title': n.xpath(".//span[@class='list__item__title']/text()")[0],
                 'source': self.source,
                 'date': html.fromstring(requests.get(n.xpath("./@href")[0].split('?')[0],
                                                      headers=self.headers).text).xpath("//span//@datetime")[0]}
            sleep(randint(1, abs(self.avg_seconds_between_attempts * 2 - 1)))
            result_news.append(result_n)
        self.print_done()
        return result_news


class LentaRuParser(NewsParser):
    def __init__(self):
        super().__init__('https://lenta.ru', 'lenta.ru')

    def get_news(self):
        result_news = []
        news = self.DOM.xpath("//div[@class='span8 js-main__content']//div[@class='span4']/div[@class='item']")
        for n in news:
            result_n = \
                {'link': self.main_link + n.xpath("./a/@href")[0],
                 'title': n.xpath("./a/text()")[0],
                 'source': self.source,
                 'date': n.xpath(".//time/@datetime")[0][1:]}
            result_news.append(result_n)
        self.print_done()
        return result_news


class YandexNewsParser(NewsParser):
    def __init__(self):
        super().__init__('https://yandex.ru/news', 'yandex/news')

    def get_news(self):
        result_news = []
        news = self.DOM.xpath("//div[@class='page-content__cell']//td[@class='stories-set__item']")
        for n in news:
            result_n = \
                {'link': 'https://yandex.ru' + n.xpath(".//a[contains(@class, 'link')]/@href")[0],
                 'title': n.xpath(".//h2[@class='story__title']/*/text()")[0],
                 'source': self.source,
                 'date': str(datetime.now().date()) + '   ' +
                         n.xpath(".//div[@class='story__date']/text()")[0].split(' ')[-1]}
            result_news.append(result_n)
        self.print_done()
        return result_news