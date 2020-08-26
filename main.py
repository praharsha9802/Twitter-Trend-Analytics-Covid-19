from TweetObject import TweetObject
from Scraper import TweetScraper
from helper import *
import pandas as pd
import pickle


class MainClass:
    def __init__(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate
        self.tweets = dict()

    def createTweetObject(self, username=None, since=None, until=None, query=None, maxTweets=None):
        tweetCriteria = TweetObject(maxTweets)
        tweetCriteria.setquerySearch(query)
        tweetCriteria.setSince(since)
        tweetCriteria.setUntil(until)
        tweetCriteria.setMaxTweets(maxTweets)
        return tweetCriteria

    def createTweetDict(self, tweet):
        temp = dict()
        temp["username"] = tweet.username
        temp["date"] = tweet.date
        temp["text"] = tweet.text
        return temp

    def dumpFile(self, fileNo):
        (pd.DataFrame.from_dict(self.tweets, orient='index')).to_csv('../Tweets/tweets'+str(fileNo)+'.csv')

    def updateTweetsAndWrite(self, tweets, fileNo):
        for tweet in tweets:
            if tweet.id in self.tweets.keys():
                continue
            else:
                self.tweets[tweet.id] = self.createTweetDict(tweet)
            if len(self.tweets) == 5000:
                self.dumpFile(fileNo)
                self.tweets = dict()
                fileNo += 1
        return fileNo

    def getTweets(self, query):
        fileNo = 67
        for start, end in daterange(self.startDate, self.endDate, False):
            tweetCriteria = self.createTweetObject(since=start, until=end, query=query, maxTweets=10000)
            scraper = TweetScraper()
            tweets = scraper.getTweets(tweetCriteria)
            print(len(tweets))
            fileNo = self.updateTweetsAndWrite(tweets, fileNo)
            del tweets
        self.dumpFile(fileNo)


if __name__ == '__main__':
    startDate = "2020-02-25"
    endDate = "2020-03-30"
    mainObject = MainClass(startDate, endDate)
    mainObject.getTweets("corona virus")



#WORDCLOUD for all days
#create cases graph with each point(date) showing the top topics(5) for that day
#clustering and get most frequent words in each cluster that are not corona virus or covid, topic modelling for each day
#chart showing usages of word in covid context
#
