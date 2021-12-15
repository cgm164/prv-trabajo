from bs4 import BeautifulSoup
from utils import send_to_server


class ScrapperElEconomista:

    def __init__(self, article: BeautifulSoup):
        self.article = article

    def cleanString(self, string: str):
        return string.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()

    def getTheme(self):
        theme = self.article.select('.articleImage a')
        if theme and len(theme) > 0:
            theme = theme[0].attrs['href']
            theme = theme.split('/')
            if theme and len(theme) > 3:
                return theme[3]
        elif len(theme) == 0:
            theme = ''
        return theme

    def getUrl(self):
        link = self.article.select('.articleImage a')
        if link and len(link) > 0:
            link = link[0].attrs['href']
        return link

    def getUrlImage(self):
        urlImage = ''
        image = self.article.select('figure img')
        if image and len(image) > 0:
            urlImage = image[0].attrs.get('data-src')
        return urlImage

    def getTitle(self):
        title = self.article.select('.articleHeadline h2')
        if title and len(title) > 0:
            title = title[0].text
        elif len(title) == 0:
            title = ''
        return title

    def getEpigrah(self):
        epigraph = self.article.select('.articleText')
        if epigraph and len(epigraph) > 0:
            epigraph = epigraph[0].text
        elif len(epigraph) == 0:
            epigraph = ''
        return epigraph

    def getDate(self):
        date = self.article.select('[itemprop=datePublished]')
        if date and len(date) > 0:
            date = date[0].text[:10]
        elif len(date) == 0:
            date = ''
        return date

    def getAuthor(self):
        author = self.article.select('.autor')
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
            'website': 'ElEconomista',
        }

send_to_server('./proxies.txt', 'https://www.eleconomista.es/ultimas-noticias/?noiphone',
               '.article', ScrapperElEconomista, 0.2, 10, 1)
