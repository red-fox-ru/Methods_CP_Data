# Les 03
# Author: Red-F0X (Panin Stanislav)
# Data create: 07.09.2021

from pymongo import MongoClient


def connect_db():
    db = MongoClient('localhost', 27017)['vacancy_db']
    collection1 = db.superjob
    collection2 = db.hh



if __name__ == '__main__':
    connect_db()








