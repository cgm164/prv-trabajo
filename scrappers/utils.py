import json
from time import sleep
from bs4 import BeautifulSoup
from random import randint, shuffle
import requests

from services.NewsService import NewsService
from termcolor import colored, COLORS

def pritter(obj):
    print(json.dumps(obj, indent=2))

def printcolor(urls, color):
    def sprint(string):
        url = urls.split('/')
        print(colored(f'[{url[2]}]', color=color),  ' - ', f'{string}')
    return sprint

def send_to_server(file_proxies, url, initial_selector, Scrapper, delay_between, delay_between_request, index_color):
    service = NewsService()
    list_colors = list(COLORS.keys())
    color = list_colors[index_color]
    sprint = printcolor(url, color)
    while True:
        with open(file_proxies, 'r') as f:
            proxies = f.readlines()
            sprint('Testing proxies...')
            shuffle(proxies)
            for proxy in proxies:
                proxy = proxy.strip()
                sprint('Testing proxy: ' + proxy)
                try:
                    response = requests.get(url)
                    i = 0
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        articles = soup.select(initial_selector)
                        for article in articles:
                            try:
                                scrapper = Scrapper(article)
                                data = scrapper.getNewsInfo()
                                service.save(data)
                                i += 1
                                sleep(delay_between)
                                sprint('Saved: ' + str(data['title']))
                            except:
                                sprint('Error in article')
                                continue
                    break
                except:
                    sprint('Proxy not working')
                    continue
        sprint('Sleeping...' + str(delay_between_request))
        sleep(delay_between_request)
