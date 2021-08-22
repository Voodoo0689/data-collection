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
import json

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                         '(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
url = 'https://hh.ru'

params = {'clusters': 'true', 'area': '1', 'ored_clusters': 'true', 'enable_snippets': 'true', 'salary': '',
          'st': 'searchVacancy', 'text': input('профессия: ')}
vacancy_list = []

response_max = requests.get(url + '/search/vacancy', params=params, headers=headers)
soup_max = bs(response_max.text, 'html.parser')
max_page = int(soup_max.find(text= '...').parent.find(rel="nofollow").text)

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

        try:
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
        except:
            salary = None
        if salary:
            salary = str(salary.split(sep=','))


        vacancy_data['name'] = name
        vacancy_data['link'] = link
        vacancy_data['salary'] = salary
        vacancy_data['url'] = url
        vacancy_list.append(vacancy_data)

pprint(vacancy_list)

with open("base.json", "w") as write_file:
    json.dump(vacancy_list, write_file)
