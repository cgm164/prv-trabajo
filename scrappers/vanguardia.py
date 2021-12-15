import requests
from bs4 import BeautifulSoup
from utils import send_to_server
from services.NewsService import NewsService
from time import sleep

class ScrapperVanguardia:

    def __init__(self, article: BeautifulSoup):
        self.article = article

    def cleanString(self, string: str):
        return string.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()

    def getTheme(self):
        theme = self.article.select('.category')
        if theme and len(theme) > 0:
            theme = theme[0].text
        elif len(theme) == 0:
            theme = ''
        return theme

    def getLink(self):
        link = self.article.select('.category p')
        if link and len(link) > 0:
            link = link[0].attrs['href']
        return link

    def getTitle(self):
        title = self.article.select('.title')
        if title and len(title) > 0:
            title = title[0].text
        elif len(title) == 0:
            title = ''
        return title

    def getDescription(self):
        description = self.article.select('.description')
        if description and len(description) > 0:
            description = description[0].text
        elif len(description) == 0:
            description = ''
        return description

    def getDate(self, link: str):
        date = ''
        if link and len(link.split('/')) > 2:
            splitedDate = link.split('/')
            index = -1
            for i in range(len(splitedDate)):
                if str.isnumeric(splitedDate[i]):
                    index = i
                    break
            if index != -1:
                date = link.split('/')[index]
                if len(date) == 8:
                    date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
        return date

    def getNewsInfo(self):
        title = self.cleanString(self.getTitle())
        description = self.cleanString(self.getDescription())
        theme = self.cleanString(self.getTheme())
        link = self.getLink()
        date = self.getDate(link)
        return {
            'title': title,
            'epigraph': description,
            'url': link,
            'urlToImage': '',
            'publishedAt': date,
            'author': '',
            'theme': theme,
            'website': 'Vanguardia',
        }

send_to_server('./proxies.txt', 'https://www.lavanguardia.com/',
               '.article-module', ScrapperVanguardia, 0.2, 10, 6)