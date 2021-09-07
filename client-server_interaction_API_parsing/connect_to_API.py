# Les 01
# Author: Red-F0X (Panin Stanislav)
# Data create: 01.09.2021


import json
import requests


# Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
class SaveUserReposJSON:
    def __init__(self, user='red-fox-ru'):
        self.api_url = 'https://api.github.com'
        self.user = user
        self.url = f'{self.api_url}/users/{user}/repos'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.159 Safari/537.36'
        }

    def get_json(self):
        self.resp = requests.get(self.url, headers=self.headers)
        with open('data.json', 'w') as f:
            json.dump(self.resp.json(), f)
        return ', '.join([el['name'] for el in self.resp.json()])


# Изучить список открытых API.
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
class AuthorizedLoginAPI:
    def __init__(self, page=1):
        self.api_url = 'https://api.kinopoisk.cloud'
        self.token = '/token/[token]' # change [token] to your token
        self.movies = '/movies/'
        self.serials = '/tv-series/'
        self.page = 'all/page/' + str(page)

    def get_movie_json(self):
        url = self.api_url + self.movies + self.page + self.token
        self.resp = requests.get(url)
        with open('kp-data.json', 'w', encoding="utf-8") as f:
            json.dump(self.resp.json(), f, ensure_ascii=False)


if __name__ == '__main__':
    usr1 = SaveUserReposJSON()
    usr1.get_json()
    usr2 = AuthorizedLoginAPI(page=2)
    usr2.get_movie_json()
