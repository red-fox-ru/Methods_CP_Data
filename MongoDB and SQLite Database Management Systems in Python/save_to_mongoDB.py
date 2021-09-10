# Les 03
# Author: Red-F0X (Panin Stanislav)
# Data create: 07.09.2021

from Parsing_HTML_Beautifulsoup import parsing_vacancy_sj_hh as data
from pymongo import MongoClient


# Развернуть у себя на компьютере MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.
def write_to_db(name_db):
    db = MongoClient('localhost', 27017)[name_db]
    db.superjob.insert_many(data.get_vacancy_sj('https://www.superjob.ru/vacancy/search/', 'python'))
    db.hh.insert_many(data.get_vacancy_hh('https://hh.ru/search/vacancy', 'python'))

# Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
def filter_vacaancy(name_db):
    db = MongoClient('localhost', 27017)[name_db]
    db.hh.find({'zp': {'$gte': 300000}})

# Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
def update_db(add_obj, name_db):
    db = MongoClient('localhost', 27017)[name_db]
    for obj in add_obj:
        db.hh.update_many(obj, {'$set': obj})


if __name__ == '__main__':
    write_to_db('vacancy_db')
    filter_vacaancy('vacancy_db')
    update_db(data.get_vacancy_hh('https://hh.ru/search/vacancy', 'python'), 'vacancy_db')
