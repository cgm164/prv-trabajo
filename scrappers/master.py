import os
from threading import Thread

listscrappers = [
    'elconfidencial.py',
    'elpais.py',
    'elmundo.py',
    'eleconomista.py',
    'larazon.py',
    'vanguardia.py',
    'expansion.py'
]

def run_scrapper(scrapper_name):
    os.system('python scrappers/' + scrapper_name)

threads = []
# In this case 'urls' is a list of urls to be crawled.
for i in range(len(listscrappers)):
    # We start one thread per url present.
    process = Thread(target=run_scrapper, args=[listscrappers[i]])
    process.start()
    threads.append(process)
# We now pause execution on the main thread by 'joining' all of our started threads.
# This ensures that each has finished processing the urls.
for process in threads:
    process.join()