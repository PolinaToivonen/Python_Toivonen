from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(String)
    points = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)


def save(pre_base):
    s = session()
    rows = s.query(News).filter(News.label is None).all()
    bd_labels = []
    for row in rows:
        bd_labels.append(row.title)
    for current_new in pre_base:
        if current_new['title'] not in bd_labels:
            news = News(title=current_new['title'],
                        author=current_new['author'],
                        url=current_new['url'],
                        points=current_new['points'],
                        comments=current_new['comments'])
            s.add(news)
    s.commit()
