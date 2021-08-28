# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные данные в БД
# Минимум один сайт, максимум - все три
#


from lxml import html
from pprint import pprint
import requests

from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['data']
news = db.news

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/92.0.4515.159 Safari/537.36'}

response = requests.get('https://lenta.ru/parts/news/', headers=header)
dom = html.fromstring(response.text)
items = dom.xpath("//div[contains(@data-more-url,'/parts/news')]")

for item in items:
    news_data = {}
    origin = item.xpath("./div/a/text()")
    name = item.xpath("./div/h3/a/text()")
    linc = item.xpath("./div/h3/a/@href")
    time = item.xpath("./div/text()")

    news_data['origin'] = origin
    news_data['name'] = name
    news_data['linc'] = linc
    news_data['time'] = time

    news.insert_one(news_data)

for i in news.find({}):
    pprint(i)
