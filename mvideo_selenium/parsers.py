from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import traceback
import time
import json

from db_connector import  DBConnector


class Parser:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('start-maximized')
        # self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.timeout_sec = 10
        self.db_connector = DBConnector('localhost', 'mvideo')

    def parse(self):
        # Переходим на главную страницу.
        self.driver.get('https://www.mvideo.ru/')

        while True:
            try:
                next_button = WebDriverWait(self.driver, self.timeout_sec).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "(//div[@data-init='gtm-push-products'])[1]"
                                                    "//a[@class='next-btn sel-hits-button-next']")))
                next_button.send_keys(Keys.RETURN)
            except:
                print('Превышено время ожидания элемента.')
                break
        goods = self.driver.find_elements_by_xpath("(//div[@data-init='gtm-push-products'])[1]"
                                                   "//li[@class='gallery-list-item']")
        for g in goods:
            a_tag = g.find_element(By.TAG_NAME, 'a')
            g_card = json.loads(a_tag.get_attribute('data-product-info'))
            g_card['link'] = a_tag.get_attribute('href')
            self.db_connector.add_hit(g_card)
            print(g_card)
        print('Хиты продаж собраны.')

