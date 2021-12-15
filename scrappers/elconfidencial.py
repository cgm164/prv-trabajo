import requests
from bs4 import BeautifulSoup
from utils import send_to_server

class ScrapperElConfidencial:

    def __init__(self, article: BeautifulSoup):
        self.article = article

    def cleanString(self, string: str):
        return string.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()

    def getTheme(self):
        return ''

    def getUrl(self):
        link = self.article.select('h2 a')
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
        title = self.article.select('.title1')
        if title and len(title) > 0:
            title = title[0].attrs['title']
        elif len(title) == 0:
            title = ''
        return title

    def getEpigrah(self):
        description = self.article.select('p')
        if description and len(description) > 0:
            description = description[0].get_text()
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
        return date

    def getAuthor(self):
        author = self.article.select('.journalist-signature')
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
            'website': 'ElConfidencial',
        }


send_to_server('./proxies.txt', 'https://www.elconfidencial.com/ultima-hora-en-vivo',
               'article', ScrapperElConfidencial, 0.2, 10, 7)
