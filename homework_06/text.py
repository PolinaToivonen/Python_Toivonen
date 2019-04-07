"""
Two functions with tests
"""
from typing import List
import string
import nltk
from textblob import TextBlob

'''
def clean(text: str) -> List[str]:
    """ Only removing punctuation and switching to lower case """
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)
    cleaned_text = [word.lower() for word in text.split()]
    return cleaned_text
    # test_SMSSpamCollection: model.score(X_test, y_test) = 0.9832535885167464
    # test_news.db: model.score(titles, labels) = 0.993421052631579
'''


def clean(text: str) -> List[str]:
    """ Removing punctuation, switching to lower case and stemming"""
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)
    tb_text = TextBlob(text)
    stop_words = nltk.corpus.stopwords.words('english')
    words_list = [word for word in tb_text.words.stem().lower()
                  if word not in stop_words]
    cleaned_text = list(set(words_list))
    return cleaned_text
    # test_SMSSpamCollection: model.score(X_test, y_test) = 0.9772727272727273
    # test_news.db: model.score(titles, labels) = 0.9967532467532467
