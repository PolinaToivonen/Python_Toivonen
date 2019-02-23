from collections import Counter
from math import log


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        labeled_words = []
        for doc, label in zip(X, y):
            for word in doc.split():
                labeled_words.append((word, label))
        self.word_lab_counted = dict(Counter(labeled_words))
        self.labels_counted = dict(Counter(y))

        words = [word for doc in X for word in doc.split()]
        self.words_counted = dict(Counter(words))

        self.info_labels = {}

        for label in self.labels_counted:
            self.info_labels[label] = {
                'number of words': self.count_words_for_label(label),
                'apr_prob': self.labels_counted[label] / len(y)
            }
        self.info_words = {}

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        answers = []

        for doc in X:
            words = doc.split()
            predictions = []

            for label in self.info_labels:
                apr_prob = self.info_labels[label]['apr_prob']
                result = log(apr_prob)

                for word in words:
                    curr_word = self.info_words.get(word)
                    if curr_word:
                        result += log(curr_word[label])

                predictions.append((result, label))

            score, predicted = max(predictions)
            answers.append(predicted)

        return answers

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        total = len(y_test)
        correct = 0
        prediction = self.predict(X_test)

        for i in range(len(prediction)):
            if prediction[i] == y_test[i]:
                correct += 1

        return correct / total

    def count_words_for_label(self, label):
        c = 0
        for word, word_label in self.word_lab_counted:
            if word_label == label:
                c += self.word_lab_counted[(word, word_label)]
        return c

    def smoothing(self, word, label):

        alpha = self.alpha
        n_ic = self.word_lab_counted.get((word, label), 0)
        n_c = self.info_labels[label]['number_of_words']
        d = len(self.words_counted)
        return (n_ic + alpha) / (n_c + alpha * d)
