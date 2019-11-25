from parsers import *
import requests
import traceback
from time import sleep
from pprint import pprint


try:
    mail_ru = MailRuParser()
    lenta_ru = LentaRuParser()
    yandex_news = YandexNewsParser()

    print('\n\nmail.ru:\n')
    pprint(mail_ru.get_news())
    print('\n\nlenta.ru:\n')
    pprint(lenta_ru.get_news())
    print('\n\nyandex/news:\n')
    pprint(yandex_news.get_news())
except:
    print(traceback.format_exc())
