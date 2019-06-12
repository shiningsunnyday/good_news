import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import numpy as np
import pdb

import matplotlib.pyplot as plt

news_csv = pd.read_csv('../OnlineNewsPopularity/OnlineNewsPopularity.csv')
urls = news_csv.url
total_batches = (len(urls) + 100) // 100

def scrape(num_batches):
    for batch in range(num_batches):
        news_scrape = []
        batch_size = 100 if batch < len(urls) // 100 else len(urls) % 100
        prog = round(100 * (batch / ((len(urls) + 100) / 100)))
        print("batch", batch, '%s%% complete' % (prog))
        author_err, tag_err, base_err = 0, 0, 0
        for i in range(batch_size):
            url = urls[100 * batch + i]
            try:
                pg = urllib.request.urlopen(url)
                pg_bytes = pg.read()
                pg_html = pg_bytes.decode('utf8')
                soup = BeautifulSoup(pg_html, "html.parser")
                try:
                    author = soup.find("span", "author_name").a.get_text()
                except AttributeError:
                    author = ""
                    author_err += 1
                result = "".join(list(map(lambda x: x.get_text(), soup.find("section", "article-content").find_all("p"))))
                try:
                    tags = soup.find("footer", "article-topics")
                    tags = list(map(lambda x: x.get_text().lower(), soup.find("footer", "article-topics").find_all("a")))
                except AttributeError:
                    tags = []
                    tag_err += 1
            except:
                base_err += 1
                pass
            news_scrape.append([url, author, result.replace('\n', ''), ','.join(tags)])
        f_write = open("news_contents.txt", 'a')
        np.savetxt(f_write, np.array(news_scrape), delimiter = '|', fmt = '%s')
        f_write.close()

def scrape_title(num_batches):
    for batch in range(num_batches):
        batch_size = 100 if batch < num_batches - 1 else len(urls) % 100
        print(batch,"of",num_batches)
        titles = []
        for i in range(batch_size):
            url = urls[100 * batch + i]
            try:
                pg = urllib.request.urlopen(url)
                pg_bytes = pg.read()
                pg_html = pg_bytes.decode('utf8')
                soup = BeautifulSoup(pg_html, "html.parser")
                titles.append([url, soup.find('title').get_text()])
            except:
                titles.append([url,""])
        f_write = open("news_title.txt", 'a')
        np.savetxt(f_write, np.array(titles), delimiter = '|', fmt = '%s')
        f_write.close()

scrape_title((news_csv.shape[0] + 100) // 100)
