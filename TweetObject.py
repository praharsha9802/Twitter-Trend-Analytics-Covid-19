class TweetObject:
    def __init__(self, maxTweets):
        self.maxTweets = maxTweets
    def setUsername(self, username):
        self.username = username
    def setSince(self, since):
        self.since = since
    def setUntil(self, until):
        self.until = until
    def setquerySearch(self, query):
        self.query = query
    def setMaxTweets(self, maxTweets):
        self.maxTweets = maxTweets
    def setTopTweets(self, topTweets):
        self.topTweets = topTweets
    def getMaxTweets(self):
        return self.maxTweets