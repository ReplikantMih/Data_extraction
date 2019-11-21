import requests
from bs4 import BeautifulSoup as BS

link = 'https://www.superjob.ru/vacancy/search/?'


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

def get_link(job_title):
    full_link = link + f'keywords={job_title}'

    user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' \
                 r' Chrome/78.0.3904.97 Safari/537.36'
    headers = {'User-Agent': user_agent}

    resp = requests.get(full_link, headers=headers)
    bs = BS(resp.text, 'lxml')
    canonical_link = bs.head.find('link', attrs={'rel': 'canonical'})['href']
    return canonical_link



# print(get_link('дизайнер'))


full_link = f'https://www.superjob.ru/vakansii/analitik.html?page=3'

user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' \
             r' Chrome/78.0.3904.97 Safari/537.36'
headers = {'User-Agent': user_agent}

resp = requests.get(full_link, headers=headers)

with open('SJ.html', 'r', encoding='utf-8') as file:
    html = file.read()

bs = BS(html, 'lxml')

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
    print(t, '   ', __sallary_from_text('', sallary), '   ', l)
