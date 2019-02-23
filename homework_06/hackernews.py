from bottle import route, run, template, request, redirect
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import string


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label is None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    label, id = request.query.label, request.query.id
    s = session()
    s.query(News).filter(News.id == id).update({'label': label})
    s.commit()
    redirect("/news")


@route("/update")
def update_news():

    news = get_news('https://news.ycombinator.com')
    s = session()

    for post in news:
        if s.query(News).filter(News.title == post['title'],
                                News.author == post['author']).first():
            break
        else:
            s.add(News(**post))
    s.commit()
    redirect("/news")


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


if __name__ == "__main__":
    s = session()
    rows = s.query(News).filter(News.label is not None).all()
    X_train = [clean(row.title).lower() for row in rows]
    y_train = [row.label for row in rows]
    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    run(host="localhost", port=8080)
