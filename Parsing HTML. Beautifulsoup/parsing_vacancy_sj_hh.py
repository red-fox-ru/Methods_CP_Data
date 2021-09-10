# Les 02
# Author: Red-F0X (Panin Stanislav)
# Data create: 07.09.2021


import unicodedata
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import lxml


# Cобирает информацию о вакансиях на вводимую должность с сайтов Superjob и HH.
# Приложение анализирует несколько страниц сайта .
# Получившийся список содержит в себе:
# - Наименование вакансии.
# - Предлагаемую зарплату (отдельно минимальную и максимальную).
# - Ссылку на саму вакансию.
# - Сайт, откуда собрана вакансия.
# - Работодатель
# - Общий результат выводится с помощью dataFrame через pandas.
def get_vacancy_sj(url, search, page=0):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.159 Safari/537.36'
    }
    r = requests.get(url, headers=headers, params={'keywords': search, 'page': page})
    r.encoding = 'utf8'
    soup = bs(r.text, 'lxml')
    links = ['https://www.superjob.ru' + el.get('href') for el in soup.find_all('a', {'class': '_6AfZ9'})]
    name = [el.get_text() for el in soup.find_all('a', {'class': '_6AfZ9'})]
    zp = [unicodedata.normalize("NFKD", el.get_text(strip=True)) for el in
          soup.find_all('span', {'class': 'f-test-text-company-item-salary'})]
    company = [el.get_text() for el in soup.find_all('a', {'class': '_205Zx'})]
    vacancy_return = []
    for num, item in enumerate(name):
        vacancy_return.append({
            'title': item,
            'url': links[num],
            'zp': zp[num],
            'company': company[num]
        })
    return vacancy_return


def get_vacancy_hh(url, search, page=0):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.159 Safari/537.36'
    }
    r = requests.get(url, headers=headers, params={'st': 'searchVacancy', 'text': search, 'page': page})
    r.encoding = 'utf8'
    soup = bs(r.text, 'lxml')
    links = [el.get('href') for el in soup.find_all('a', {'data-qa': 'vacancy-serp__vacancy-title'})]
    name_zp = [unicodedata.normalize("NFKD", el.get_text('|', strip=True)) for el in
               soup.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})]
    name = []
    zp = []
    for el in name_zp:
        if len(el.split('|')) > 1:
            name.append(el.split('|')[0])
            zp.append(el.split('|')[1])
        else:
            name.append(el)
            zp.append('')
    company = [unicodedata.normalize("NFKD", el.get_text()) for el in
               soup.find_all('a', {'data-qa': 'vacancy-serp__vacancy-employer'})]

    vacancy_return = []
    for num, item in enumerate(name):
        vacancy_return.append({
            'title': item,
            'url': links[num],
            'zp': zp[num],
            'company': company[num]
        })
    return vacancy_return


if __name__ == '__main__':
    all_vacancy = []
    for page in range(5):
        all_vacancy += get_vacancy_sj('https://www.superjob.ru/vacancy/search/', 'python', page)
        all_vacancy += get_vacancy_hh('https://hh.ru/search/vacancy', 'python', page)
    pd.DataFrame(all_vacancy).to_csv('vacancy.csv', index=False)
