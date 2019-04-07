"""
Testing and compare
"""
import csv
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from bayes import NaiveBayesClassifier
from db import News, session

# test_SMSSpamCollection
with open("data\\SMSSpamCollection", encoding='utf-8') as f:
    data = list(csv.reader(f, delimiter="\t"))
X, y = [], []
for target, msg in data:
    X.append(msg)
    y.append(target)
X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

# with MultinomialNB
model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB(alpha=0.05)),
])
model.fit(X_train, y_train)
print(model.score(X_test, y_test))

# with NaiveBayesClassifier
model = NaiveBayesClassifier()
model.fit(X_train, y_train)
print(model.score(X_test, y_test))

# test_news.db
s = session()
rows = s.query(News).filter(News.label != None).all()
labels = [row.label for row in rows]
titles = [row.cleaned for row in rows]

# with MultinomialNB
model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB(alpha=0.05)),
])
model.fit(titles, labels)
print(model.score(titles, labels))

# with NaiveBayesClassifier
model = NaiveBayesClassifier()
model.fit(titles, labels)
print(model.score(titles, labels))
