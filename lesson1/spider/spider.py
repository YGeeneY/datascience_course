import requests
import csv
import logging
from os import path
from time import sleep

from bs4 import BeautifulSoup


base_dir = path.dirname(path.abspath(__file__))


logging.basicConfig(
    filename=path.join(base_dir, '4pda_spider.log'),
    level=logging.INFO,
)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
console.setFormatter(formatter)

logging.getLogger("").addHandler(console)


root_url = 'http://4pda.ru/page/'


def get_4pda_page(page_num):
    logging.info('page num:{} crawling started'.format(page_num))
    url = root_url + str(page_num)
    response = requests.get(url)
    if response.status_code != 200:
        logging.critical('fail to load url ' + root_url)
    logging.debug('content length {}'.format(len(response.text)))
    return response.text


def parse_4pda_page(html):
    logging.info('parsing started')
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', attrs={'class': 'post'})

    # first article is a commercial
    for article in articles[1:]:

        article = dict(
            title=article.find('div', attrs={'class': 'visual'}).find('a')['title'],
            date_published=article.find('meta', attrs={'itemprop': 'datePublished'})['content'],
            author=article.find('span', attrs={'class': 'autor'}).text,
            # tags=[tag.text for tag in article.find_all('a', attrs={'rel': 'tag'})],
            comments_count=int(article.find('a', attrs={'class': 'v-count'}).text)
        )

        yield {k: unicode(v).encode('utf-8') for k, v in article.iteritems()}
    logging.info('parsing done')


def run(page_num):
    f = open(path.join(base_dir, '4pda_dump.csv'), 'wb')
    headers = ['title', 'date_published', 'author',
               # 'tags',
               'comments_count']
    writer = csv.DictWriter(f, headers)
    writer.writeheader()
    for page in range(page_num):
        html = get_4pda_page(page)
        sleep(0.3)
        articles = parse_4pda_page(html)
        for article in articles:
            writer.writerow(article)
    f.close()


if __name__ == '__main__':
    run(1000)
