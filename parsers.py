import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import pandas as pd


class Parser:
    def __init__(self):
        self.user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' \
                          r' Chrome/78.0.3904.97 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}


class HHParser(Parser):
    def __init__(self, job_title):
        super().__init__()
        self.job_title = job_title
        self.link = 'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true'
        self.list_pages_to_parse = 5

        self.jobs = []
        self.jobs_dataframe = None

    def run_loop(self):
        for index in range(self.list_pages_to_parse):
            full_link = f'{self.link}&text={"+".join(self.job_title.split(" "))}&page={index}'

            html = requests.get(full_link, headers=self.headers).text

            bs = BeautifulSoup(html, 'lxml')
            jobs = bs.find('div', {'class': 'vacancy-serp'})
            jobs_list = jobs.findChildren(attrs={'data-qa': 'vacancy-serp__vacancy'})

            for j in jobs_list:
                if j:
                    name_link_sallary = j.find(attrs=['vacancy-serp-item__row vacancy-serp-item__row_header'])
                    job = {}
                    job['name'] = name_link_sallary.find(attrs=['g-user-content']).a.text
                    job['link'] = name_link_sallary.find(attrs=['g-user-content']).a['href']
                    sallary_text = name_link_sallary.find(attrs=['vacancy-serp-item__sidebar']).text
                    job['sallary_from'] = \
                    self.__sallary_from_text(sallary_text)[0]
                    job['sallary_till'] = \
                    self.__sallary_from_text(sallary_text)[1]
                    job['site'] = 'hh.ru'
                    self.jobs.append(job)
            print(f'hh.ru parser: page {index + 1} from {self.list_pages_to_parse} - Done.')
            sleep(randint(1, 10))
        self.jobs_dataframe = pd.DataFrame.from_dict(self.jobs)
        print(self.jobs_dataframe)

    def __sallary_from_text(self, sallary):
        if not sallary:
            return -1, -1
        sallary = ''.join(sallary.split())
        if 'от' in sallary:
            sallary = sallary.replace('от', '').replace('руб.', '')
            return int(sallary), -1
        if 'до' in sallary:
            sallary = sallary.replace('до', '').replace('руб.', '')
            return -1, int(sallary)
        if '-' in sallary:
            sallary = sallary.replace('руб.', '')
            sallary = sallary.split('-')
            return int(sallary[0]), int(sallary[1])


class SuperjobParser(Parser):
    def __init__(self, job_title):
        super().__init__()
        self.job_title = job_title
        self.link = self.__get_link('+'.join(self.job_title.split(' ')))
        self.list_pages_to_parse = 5

        self.jobs = []
        self.jobs_dataframe = None

    def run_loop(self):
        for index in range(self.list_pages_to_parse):
            full_link = f'{self.link}&page={index}'
            html = requests.get(full_link, headers=self.headers).text
            bs = BeautifulSoup(html, 'lxml')

            jobs = bs.find_all('div', attrs={'class': 'f-test-vacancy-item'})

            for job in jobs:
                sallary = job.find('span', attrs={'class': 'f-test-text-company-item-salary'}).text
                titles = job.find_all('a')
                t = None
                for title in titles:
                    if 'vakansii' in title['href']:
                        t = title.text
                links = job.find_all('a')  # ['href']
                l = None
                for link in links:
                    if 'vakansii' in link['href']:
                        l = link['href']
                sallary = self.__sallary_from_text(sallary)
                job_ = {}
                job_['name'] = t
                job_['link'] = 'https://www.superjob.ru' + l
                job_['sallary_from'] = sallary[0]
                job_['sallary_till'] = sallary[1]
                job_['site'] = 'superjob.ru'
                self.jobs.append(job_)
            print(f'superjob.ru parser: page {index + 1} from {self.list_pages_to_parse} - Done.')
            sleep(randint(1, 10))
        self.jobs_dataframe = pd.DataFrame.from_dict(self.jobs)
        print(self.jobs_dataframe)

    def __sallary_from_text(self, sallary):
        if not sallary or 'договорённости' in sallary:
            return -1, -1
        sallary = ''.join(sallary.split())
        if 'от' in sallary:
            sallary = sallary.replace('от', '').replace('₽', '')
            return int(sallary), -1
        if 'до' in sallary:
            sallary = sallary.replace('до', '').replace('₽', '')
            return -1, int(sallary)
        if '—' in sallary:
            sallary = sallary.replace('₽', '')
            sallary = sallary.split('—')
            return int(sallary[0]), int(sallary[1])
        return (-1, -1)

    def __get_link(self, job_title):
        tmp_link = 'https://www.superjob.ru/vacancy/search/'
        full_link = tmp_link + f'?keywords={job_title}'

        resp = requests.get(full_link, headers=self.headers)
        bs = BeautifulSoup(resp.text, 'lxml')
        canonical_link = bs.head.find('link', attrs={'rel': 'canonical'})['href']
        if canonical_link == tmp_link:
            return f'{canonical_link}?keywords={job_title}'
        return canonical_link + '?'
