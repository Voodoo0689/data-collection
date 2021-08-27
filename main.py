# Вариант 1
# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайтов HH(обязательно)
# и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта
# (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с
# помощью dataFrame через pandas. Сохраните в json либо csv.
import hashlib
import json

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['vacancys_HH']
jobs = db.jobs

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                         '(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
url = 'https://hh.ru'

params = {'clusters': 'true', 'area': '1', 'ored_clusters': 'true', 'enable_snippets': 'true', 'salary': '',
          'st': 'searchVacancy', 'text': 'Python'}
# vacancy_list = []

response_max = requests.get(url + '/search/vacancy', params=params, headers=headers)
soup_max = bs(response_max.text, 'html.parser')
max_page = int(soup_max.find(text='...').parent.find(rel="nofollow").text)


def get_data():
    for x in range(max_page):
        params['page'] = f'{x}'

        response = requests.get(url + '/search/vacancy', params=params, headers=headers)
        soup = bs(response.text, 'html.parser')
        vacancys = soup.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

        for vacancy in vacancys:
            vacancy_data = {}
            info = vacancy.find(target="_blank")
            name = info.text
            link = info['href']
            _id = hashlib.sha1(link.encode('utf-8')).hexdigest()
            vacancy_data['_id'] = _id
            vacancy_data['name'] = name
            vacancy_data['link'] = link
            vacancy_data['url'] = url
            vacancy_data['_id'] = _id

            try:
                salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text

                # print(vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}))

                if salary[:2] == 'от':
                    salary_max = None
                    salary_min = int(salary[3:salary.rfind(' ')].replace('\u202f', ''))
                    # print(salary_min)
                    # print(salary_max)
                elif salary[:2] == 'до':
                    salary_min = None
                    salary_max = int(salary[3:salary.rfind(' ')].replace(u'\u202f', ''))
                else:
                    salary_min = int(salary[:salary.find(' – ')].replace('\u202f', ''))
                    salary_max = int(salary[salary.find(' – ') + 3:salary.rfind(' ')].replace('\u202f', ''))
                    # print(salary_min)
                    # print(salary_max)
                currency = salary[salary.rfind(' ') + 1:]
                vacancy_data['salary_min'] = salary_min
                vacancy_data['salary_max'] = salary_max
                vacancy_data['currency'] = currency
                jobs.insert_one(vacancy_data)
            except:
                continue

        # vacancy_list.append(vacancy_data)
# pprint(vacancy_list)

# with open("base.json", "w", encoding='UTF-8') as write_file:
#     json.dump(vacancy_list, write_file, ensure_ascii=False)
#
# for i in jobs.find({}):
#     pprint(i)
