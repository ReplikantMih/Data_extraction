from bs4 import BeautifulSoup as BS
import json
import requests

user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
headers = {'User-Agent': user_agent}
#
resp = requests.get('https://krasnodar.hh.ru/search/vacancy?area=1&st=searchVacancy&text=Data+scientist&from=suggest_post', headers=headers)
code = resp.status_code
# text = resp.text
#
# with open('data\hh_list.html', 'w', encoding='utf-8') as file:
#     file.write(text)

# input('waiting...')

with open('data\hh_list.html', 'r', encoding='utf-8') as file:
    html = file.read()

bs = BS(html, 'lxml')
jobs = bs.find('div', {'class': 'vacancy-serp'})
jobs_list = jobs.findChildren(attrs={'data-qa': 'vacancy-serp__vacancy'})

jobs_json = []


def sallary_from_text(sallary):
    if not sallary:
        return 0, 0
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


for j in jobs_list:
    if j:
        name_link_sallary = j.find(attrs=['vacancy-serp-item__row vacancy-serp-item__row_header'])
        job = {}
        job['name'] = name_link_sallary.find(attrs=['g-user-content']).a.text
        job['link'] = name_link_sallary.find(attrs=['g-user-content']).a['href']
        job['sallary_from'] = sallary_from_text(name_link_sallary.find(attrs=['vacancy-serp-item__sidebar']).text)[0]
        job['sallary_till'] = sallary_from_text(name_link_sallary.find(attrs=['vacancy-serp-item__sidebar']).text)[1]
        job['site'] = 'hh.ru'
        print(job['sallary_from'])
        print(job['sallary_till'])
        jobs_json.append(job)

print(jobs_json)
# while True:
#     if job is not None:
#         print('DBG')
#         print(type(job))
#         job = job.next_sibling()
#     else:
#         job = jobs.find('div', {'data-qa': 'vacancy-serp__vacancy'})
#         print(type(job))
# print(job)