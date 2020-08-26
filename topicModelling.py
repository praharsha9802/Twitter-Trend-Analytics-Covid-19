import pandas as pd
from nltk.corpus import stopwords
import re
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
import sys


class TopicModel:
    def __init__(self, date, path):
        self.date = date
        self.path = path
        self.corpus = []
        self.stopwords = set(stopwords.words("english"))

    def formCorpus(self):
        dataFrame = pd.read_csv(self.path + 'combinedTweets.csv')
        dataFrame = dataFrame[(dataFrame.date == self.date) & (~(dataFrame.text.isnull()))].loc[:, ['text']]
        self.corpus = list(dataFrame.text)

    def processCorpus(self):
        for i in range(len(self.corpus)):
            self.corpus[i] = self.corpus[i].lower()
            wordList = re.findall('\w+(?:\.?\w)*', self.corpus[i])
            tokenized = [word for word in wordList if word not in self.stopwords]
            self.corpus[i] = tokenized

    def getCorpusDictionary(self):
        corpusDt = Dictionary(self.corpus)
        corpusBoW = [corpusDt.doc2bow(tweet) for tweet in self.corpus]
        return corpusBoW, corpusDt

    def performLDA(self):
        self.formCorpus()
        self.processCorpus()
        inputCorpus, vocabulary = self.getCorpusDictionary()
        tweetModel = LdaModel(inputCorpus, num_topics = 7, id2word = vocabulary)
        return tweetModel

    def saveModel(self, tweetModel):
        tweetModel.save('Models/'+self.date)

    def printTopics(self, tweetModel):
        topics = tweetModel.print_topics()
        return topics
