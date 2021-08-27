from pprint import pprint
from pymongo import MongoClient

import main
user_input = int(input('Желаемый уровень зарплаты:'))
main.get_data()


client = MongoClient('127.0.0.1', 27017)
db = client['vacancys_HH']
jobs = db.jobs


def get_a_high_paying_job(pay):
    for i in jobs.find({'currency': 'руб.', '$or': [{'salary_min': {'$gte': pay}}, {'salary_max': {'$gte': pay}}]}):
        pprint(i)
    for j in jobs.find(
            {'currency': 'USD', '$or': [{'salary_min': {'$gte': pay / 75}}, {'salary_max': {'$gte': pay / 75}}]}):
        pprint(j)


get_a_high_paying_job(user_input)
