import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep
from db_connector import DBConnector
from datetime import datetime


class Parser:
    def __init__(self):
        self.user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' \
                          r' Chrome/78.0.3904.97 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.db_connector = DBConnector(host='localhost', db='jobs_parsed')

    def add_job(self, job):
        self.db_connector.add_job(job)

    def add_unique_job(self, job):
        self.db_connector.add_unique_job(job)


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

            resp = requests.get(full_link, headers=self.headers)
            if resp.status_code != 200:
                break
            html = resp.text

            bs = BeautifulSoup(html, 'lxml')
            jobs = bs.find('div', {'class': 'vacancy-serp'})
            jobs_list = jobs.findChildren(attrs={'data-qa': 'vacancy-serp__vacancy'})

            for j in jobs_list:
                if j:
                    name_link_salary = j.find(attrs=['vacancy-serp-item__row vacancy-serp-item__row_header'])
                    job = {}
                    job['name'] = name_link_salary.find(attrs=['g-user-content']).a.text
                    job['link'] = name_link_salary.find(attrs=['g-user-content']).a['href']
                    job['site_id'] = job['link'].split('?')[0].split('/')[-1]
                    salary_text = name_link_salary.find(attrs=['vacancy-serp-item__sidebar']).text
                    try:
                        job['salary_from'] = \
                        self.__salary_from_text(salary_text)[0]
                    except:
                        continue

                    job['salary_till'] = \
                    self.__salary_from_text(salary_text)[1]
                    job['site'] = 'hh.ru'
                    job['datetime'] = datetime.now()
                    self.jobs.append(job)
                    self.add_unique_job(job)
            print(f'hh.ru parser: page {index + 1} from {self.list_pages_to_parse} - Done.')
            sleep(randint(1, 10))

    def __salary_from_text(self, salary):
        if not salary:
            return -1, -1
        salary = ''.join(salary.split())
        if 'от' in salary:
            salary = salary.replace('от', '').replace('руб.', '')
            return int(salary), -1
        if 'до' in salary:
            salary = salary.replace('до', '').replace('руб.', '')
            return -1, int(salary)
        if '-' in salary:
            salary = salary.replace('руб.', '')
            salary = salary.split('-')
            return int(salary[0]), int(salary[1])


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
            resp = requests.get(full_link, headers=self.headers)
            if resp.status_code != 200 or 'По заданным параметрам нет подходящих вакансий' in resp.text:
                break
            html = resp.text
            bs = BeautifulSoup(html, 'lxml')

            jobs = bs.find_all('div', attrs={'class': 'f-test-vacancy-item'})

            for job in jobs:
                salary = job.find('span', attrs={'class': 'f-test-text-company-item-salary'}).text
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
                try:
                    salary = self.__salary_from_text(salary)
                except:
                    continue
                job_ = {}
                job_['name'] = t
                job_['link'] = 'https://www.superjob.ru' + l
                job_['site_id'] = job_['link'].split('.')[-2].split('-')[-1]
                job_['salary_from'] = salary[0]
                job_['salary_till'] = salary[1]
                job_['site'] = 'superjob.ru'
                job_['datetime'] = datetime.now()
                self.jobs.append(job_)
                self.add_unique_job(job_)
            print(f'superjob.ru parser: page {index + 1} from {self.list_pages_to_parse} - Done.')
            sleep(randint(1, 10))

    def __salary_from_text(self, salary):
        if not salary or 'договорённости' in salary:
            return -1, -1
        salary = ''.join(salary.split())
        if 'от' in salary:
            salary = salary.replace('от', '').replace('₽', '')
            return int(salary), -1
        if 'до' in salary:
            salary = salary.replace('до', '').replace('₽', '')
            return -1, int(salary)
        if '—' in salary:
            salary = salary.replace('₽', '')
            salary = salary.split('—')
            return int(salary[0]), int(salary[1])
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
