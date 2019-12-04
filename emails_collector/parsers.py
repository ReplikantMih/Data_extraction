from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import traceback
import time
import json

from db_connector import DBConnector


class EmailCollector:
    def __init__(self):
        self.link = 'https://mail.ru'
        self.login = 'ml_geekbrains'
        self.password = 'ml1237'
        self.chrome_options = Options()
        self.chrome_options.add_argument('start-maximized')
        # self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.timeout_sec = 10
        self.db_connector = DBConnector('localhost', 'my_emails')

    def collect(self):
        self.driver.get(self.link)  # Главная страница.

        login = WebDriverWait(self.driver, self.timeout_sec).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='mailbox:login']")))
        login.send_keys(self.login)

        password = WebDriverWait(self.driver, self.timeout_sec).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='o-control']")))
        password.click()

        password = WebDriverWait(self.driver, self.timeout_sec).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='mailbox:password']")))
        password.send_keys(self.password)
        password.submit()

        letters = WebDriverWait(self.driver, self.timeout_sec).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'llc ')]")))
        letters = [letter.get_attribute('href') for letter in letters]

        for letter in letters:
            self.driver.get(letter)

            letter_detailed = WebDriverWait(self.driver, self.timeout_sec).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'thread ')]")))

            letter_db = {
                'title': letter_detailed.find_element_by_xpath("//h2[@class='thread__subject']").text,
                'body': letter_detailed.find_element_by_xpath("//div[contains(@id, '_BODY')]").text,
                'from': letter_detailed.find_element_by_xpath("//span[@class='letter__contact-item']").
                    get_attribute('title'),
                'date': letter_detailed.find_element_by_xpath("//div[@class='letter__date']").text
            }
            self.db_connector.add_letter(letter_db)
        print('Письма собраны.')