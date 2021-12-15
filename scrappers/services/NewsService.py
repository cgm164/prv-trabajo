import requests


class NewsService:

    def __init__(self):
        self.URL_API = 'http://localhost:3333/api/news'

    def save(self, news):
        requests.post(self.URL_API, data=news)
