from bs4 import BeautifulSoup
from utils import send_to_server

class ScrapperLaRazon:

    def __init__(self, article: BeautifulSoup):
        self.article = article

    def cleanString(self, string: str):
        return string.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()

    def getTheme(self):
        theme = self.article.select('.card__tag')
        if theme and len(theme) > 0:
            theme = theme[0].text
        elif len(theme) == 0:
            theme = ''
        return theme

    def getUrl(self):
        link = self.article.select('.card__image a')
        if link and len(link) > 0:
            link = link[0].attrs['href']
        return link

    def getUrlImage(self):
        urlImage = ''
        image = self.article.select('.img-reserved-space img')
        if image and len(image) > 0:
            urlImage = image[0].attrs['src']
        return urlImage

    def getTitle(self):
        title = self.article.select('.card__headline a')
        if title and len(title) > 0:
            title = title[0].attrs['aria-label']
        elif len(title) == 0:
            title = ''
        return title

    def getEpigrah(self):
        epigrah = self.article.select('.card__subheadline')
        if epigrah and len(epigrah) > 0:
            epigrah = epigrah[0].text
        elif len(epigrah) == 0:
            return self.getTitle()
        return epigrah

    def getDate(self):
        date = self.article.select('.card__byline time')
        if date and len(date) > 0:
            date = date[0].attrs['datetime'][:10]
        elif len(date) == 0:
            date = ''
        return date

    def getAuthor(self):
        author = self.article.select('.card__byline ul')
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
        date = self.getDate()
        return {
            'title': title,
            'epigraph': epigrah,
            'url': url,
            'urlToImage': urlImage,
            'publishedAt': date,
            'author': author,
            'theme': theme,
            'website': 'LaRazon',
        }


send_to_server('./proxies.txt', 'https://www.larazon.es',
               'article', ScrapperLaRazon, 0.2, 10, 5)
