import requests
from bs4 import BeautifulSoup
from utils import send_to_server
from services.NewsService import NewsService
from time import sleep

class ScrapperElMundo:

    def __init__(self, article: BeautifulSoup):
        self.article = article

    def cleanString(self, string: str):
        return string.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()

    def getTheme(self):
        theme = self.article.select('.ue-c-cover-content__kicker')
        if theme and len(theme) > 0:
            theme = theme[0].text
        elif len(theme) == 0:
            theme = ''
        return theme

    def getUrl(self):
        link = self.article.select('.ue-c-cover-content__link')
        if link and len(link) > 0:
            link = link[0].attrs['href']
        return link

    def getUrlImage(self):
        urlImage = ''
        image = self.article.select('figure img')
        if image and len(image) > 0:
            urlImage = image[0].attrs['src']
        return urlImage

    def getTitle(self):
        title = self.article.select('.ue-c-cover-content__headline')
        if title and len(title) > 0:
            title = title[0].text
        elif len(title) == 0:
            title = ''
        return title

    def getEpigrah(self):
        return self.getTitle()

    def getDate(self):
        date = self.article.select('.ue-c-cover-content__published-date')
        if date and len(date) > 0:
            date = date[0].attrs['data-publish'][:10]
        elif len(date) == 0:
            date = ''
        return date

    def getAuthor(self):
        author = self.article.select('.ue-c-cover-content__byline-name')
        if author and len(author) > 0:
            author = author[0].text
            author = author.split(':')
            if author and len(author) > 1:
                author = author[1]
        elif len(author) == 0:
            author = ''
        return author

    def getNewsInfo(self):
        title = self.cleanString(self.getTitle())
        epigrah = self.cleanString(self.getEpigrah())
        theme = self.cleanString(self.getTheme())
        author = self.cleanString(self.getAuthor())
        url = self.getUrl()
        urlImage = self.getUrlImage()
        date = self.getDate()
        return {
            'title': title,
            'epigraph': epigrah,
            'url': url,
            'urlToImage': urlImage,
            'publishedAt': date,
            'author': author,
            'theme': theme,
            'website': 'ElMundo',
        }


send_to_server('./proxies.txt', 'https://www.elmundo.es/ultimas-noticias.html',
               'article', ScrapperElMundo, 0.2, 10, 2)
