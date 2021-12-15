import requests
from bs4 import BeautifulSoup
from utils import send_to_server

class ScrapperElPais:

    def __init__(self, article: BeautifulSoup):
        self.article = article

    def cleanString(self, string: str):
        return string.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()

    def getTheme(self):
        theme = self.article.select('.c_k')
        if theme and len(theme) > 0:
            theme = theme[0].text
        elif len(theme) == 0:
            theme = ''
        return theme

    def getUrl(self):
        link = self.article.select('.c_t a')
        if link and len(link) > 0:
            link = link[0].attrs['href']
        return link

    def getUrlImage(self):
        urlImage = ''
        image = self.article.select('.a_m-h img')
        if image and len(image) > 0:
            urlImage = image[0].attrs['src']
        return urlImage

    def getTitle(self):
        title = self.article.select('.c_t')
        if title and len(title) > 0:
            title = title[0].text
        elif len(title) == 0:
            title = ''
        return title

    def getEpigrah(self):
        description = self.article.select('.c_d')
        if description and len(description) > 0:
            description = description[0].text
        elif len(description) == 0:
            description = ''
        return description

    def getDate(self, url: str):
        date = ''
        if url and len(url.split('/')) > 2:
            splitedDate = url.split('/')
            index = -1
            for i in range(len(splitedDate)):
                string = splitedDate[i].replace(
                    '-', '').replace('.', '').replace('_', '').replace(' ', '')
                if str.isnumeric(string):
                    index = i
                    break
            if index != -1:
                date = url.split('/')[index]
                if len(date) == 8:
                    date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
        return date

    def getAuthor(self):
        author = self.article.select('.c_a_a')
        if author and len(author) > 0:
            author = author[0].text
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
        date = self.getDate(url)
        return {
            'title': title,
            'epigraph': epigrah,
            'url': url,
            'urlToImage': urlImage,
            'publishedAt': date,
            'author': author,
            'theme': theme,
            'website': 'ElPais',
        }


send_to_server('./proxies.txt', 'https://www.elpais.com/ultimas-noticias/',
               'article', ScrapperElPais, 0.2, 10, 3)
