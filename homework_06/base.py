from scraputils import get_news
from db import News, session

if __name__ == "__main__":
    NEWS = get_news("https://news.ycombinator.com/newest", 34)
    S = session()
    for new in NEWS:
        record = News(title=new['title'],
                      author=new['author'],
                      url=new['url'],
                      comments=new['comments'],
                      points=new['points'],
                      cleaned=new['cleaned'])
        S.add(record)
    S.commit()
    
