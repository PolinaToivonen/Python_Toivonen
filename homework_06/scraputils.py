import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    first_row = parser.find_all('tr', attrs={'class': 'athing'})
    second_row = parser.find_all('td', attrs={'class': 'subtext'})
    n = 0
    while True:
        try:
            author = second_row[n].find('a', attrs={'class': 'hnuser'}).get_text()
            comments = second_row[n].find_all('a')[-1].get_text()
            points = second_row[n].findAll('span')[0].text.split()[0]
            title = first_row[n].find('a', attrs={'class': 'storylink'}).get_text()
            url = first_row[n].findAll('a')[1]['href']
            news_list.append({
                'author': author,
                'comments': 0 if 'discuss' in comments else int(comments.split('\xa0')[0]),
                'points': int(points),
                'title': title,
                'url': url if 'http' in url else None
                })
            n += 1
        except:
            break
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    try:
        return parser.findAll('table')[2].findAll('tr')[-1].a['href']
    except TypeError:
        return None


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html5lib")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        if type(next_page) == str:
            url = "https://news.ycombinator.com/" + next_page
            news.extend(news_list)
            n_pages -= 1
        else:
            n_pages = False
    return news
