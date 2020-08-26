from topicModelling import TopicModel
from helper import *

class TrendAnalysis:
    def __init__(self, startDate, endDate, path):
        self.startDate = startDate
        self.endDate = endDate
        self.path = path

    def createLDAObject(self, curDate):
        topicModel = TopicModel(curDate, self.path)
        return topicModel

    def saveAndPrintTopics(self):
        for start, end in daterange(self.startDate, self.endDate, True):
            ldaModel = self.createLDAObject(start)
            topicModel = ldaModel.performLDA()
            ldaModel.saveModel(topicModel)
            print(ldaModel.printTopics(topicModel))


if __name__ == '__main__':
    trends = TrendAnalysis('25-01-2020', '31-01-2020', '../Tweets/')
    trends.saveAndPrintTopics()

