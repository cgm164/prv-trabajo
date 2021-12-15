from bs4 import BeautifulSoup
from utils import send_to_server


class ScrapperExpasion:

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
        link = self.article.select('header a')
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
        title = self.article.select('header .ue-c-cover-content__headline')
        if title and len(title) > 0:
            title = title[0].text
        elif len(title) == 0:
            title = ''
        return title

    def getEpigrah(self):
        return self.getTitle()

    def getDate(self, url):
        date = url
        if date and len(date) > 0:
            if date:
                # Extract date this format https://www.expansion.com/empresas/distribucion/2021/12/15/61b98c41468aeb03418b4604.html
                date = date.split('/')
                if date and len(date) > 3:
                    for i in range(len(date)):
                        if date[i].isdigit():
                            year = date[i]
                            month = date[i + 1]
                            day = date[i + 2]
                            date = year + '-' + month + '-' + day
                            return date
                    return ''
                else:
                    return ''
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
        date = self.getDate(url)
        return {
            'title': title,
            'epigraph': epigrah,
            'url': url,
            'urlToImage': urlImage,
            'publishedAt': date,
            'author': author,
            'theme': theme,
            'website': 'Expansion',
        }


send_to_server('./proxies.txt', 'https://www.expansion.com/',
               'article', ScrapperExpasion, 0.2, 10, 4)
