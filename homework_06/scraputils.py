import requests
from bs4 import BeautifulSoup
import re


def get_page(url):
    try:
        response = requests.get(url)
        if response.ok:
            return response.text
        else:
            print("Error " + str(response.status_code))
            return False
    except requests.exceptions.ConnectTimeout:
        print('Oops. Connection timeout occured!')
    except requests.exceptions.ReadTimeout:
        print('Oops. Read timeout occured')
    except requests.exceptions.ConnectionError:
        print('Seems like dns lookup failed..')


def extract_news(url):
    """ Extract news from a given web page """
    news_list = []
    response = get_page(url)
    page = BeautifulSoup(response, 'html5lib')
    tables = page.table.findAll('table')[1].findAll('tr', {'class': 'athing'})
    for i in range(len(tables)):
        id = 'item?id=' + tables[i]['id']
        new = {'title': page.findAll('a', {'class': 'storylink'})[i].text,
               'url': page.findAll('a', {'class': 'storylink'})[i]['href'],
               'author': page.findAll('a', {'class': 'hnuser'})[i].text,
               'points': page.findAll('span', {'class': 'score'})[i].text,
               'comments': page.findAll('a', {'href': id})[-1].text}
        news_list.append(new)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.table.findAll('table')[1].findAll('a')[-1]['href']


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        parser = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(url)
        next_page = extract_next_page(parser)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


def split_row(string):
    return list(filter(None, re.split('\W|\d', string)))
