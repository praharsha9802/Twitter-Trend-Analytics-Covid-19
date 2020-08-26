from urllib.parse import quote
import sys
from urllib.request import HTTPCookieProcessor
from urllib.request import build_opener
from urllib.request import ProxyHandler
import http.cookiejar as cookielib
import json
from pyquery import PyQuery
import re
from Tweet import Tweet
from TweetObject import TweetObject
from datetime import datetime
import time

class TweetScraper:
    def __init__(self):
        pass

    def createJsonObject(self, tweetObject, scrollObject, cookieJarObject, proxy = None):

        if hasattr(tweetObject, 'topTweets'):
            if tweetObject.topTweets:
                url = "https://twitter.com/i/search/timeline?q=%s&src=typd&max_position=%s"
        else:
            url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"
        urlGetData = ''

        if hasattr(tweetObject, 'username'):
            urlGetData += ' from:' + tweetObject.username

        if hasattr(tweetObject, 'since'):
            urlGetData += ' since:' + tweetObject.since

        if hasattr(tweetObject, 'until'):
            urlGetData += ' until:' + tweetObject.until

        if hasattr(tweetObject, 'query'):
            urlGetData += ' ' + tweetObject.query

        url = url % (quote(urlGetData), quote(scrollObject))
        headers = [
            ('Host', "twitter.com"),
            ('User-Agent',
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"),
            ('Accept', "application/json, text/javascript, */*; q=0.01"),
            ('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
            ('X-Requested-With', "XMLHttpRequest"),
            ('Referer', url),
            ('Connection', "keep-alive")]
        if proxy:
            opener = build_opener(ProxyHandler({'http': proxy, 'https': proxy}),
                                                 HTTPCookieProcessor(cookieJarObject))
        else:
            opener = build_opener(HTTPCookieProcessor(cookieJarObject))
        opener.addheaders = headers
        try:
            response = opener.open(url)
            jsonResponse = response.read()
        except Exception as e:
            print(
                "Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd" % quote(urlGetData))
            print(e)
            #sys.exit(1)
            return None

        dataJson = json.loads(jsonResponse)

        return dataJson

    def getTweets(self, tweetObject, receiveBuffer = None, bufferLength = 500):
        scrollId = ''
        results = []
        resultsAux = []
        cookieJar = cookielib.CookieJar()

        if hasattr(tweetObject, 'username') and \
                (tweetObject.username.startswith("\'") or tweetObject.username.startswith("\"")) and\
                (tweetObject.username.endswith("\'") or tweetObject.username.endswith("\"")):
            tweetObject.username = tweetObject.username[1:-1]

        active = True
        while active:
            time.sleep(0.7)
            json = self.createJsonObject(tweetObject, scrollId, cookieJar)
            if not(json) or (len(json['items_html'].strip()) == 0):
                break

            scrollId = json['min_position']
            scrapedTweets = PyQuery(json['items_html'])('div.js-stream-tweet')
            scrapedTweets.remove('div.withheld-tweet')
            tweets = scrapedTweets('div.js-stream-tweet')

            if len(tweets) == 0:
                break

            for tweetHTML in tweets:
                tweetPQ = PyQuery(tweetHTML)
                tweet = Tweet()
                try:
                    txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'))
                    dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))
                    dateSec = datetime.utcfromtimestamp(dateSec).strftime('%Y-%m-%d')
                    id = tweetPQ.attr("data-tweet-id")
                    permalink = tweetPQ.attr("data-permalink-path")
                    user_id = int(tweetPQ("a.js-user-profile-link").attr("data-user-id"))
                except:
                    print(tweetHTML)
                    continue
                tweet.id = id
                tweet.userid = user_id
                tweet.permalink = 'https://twitter.com' + permalink
                tweet.username = permalink.split('/')[1]
                tweet.text = txt
                tweet.date = dateSec
                if "span class=\"Icon Icon--verified\"" in str(tweetPQ):
                    tweet.verified = True
                else:
                    tweet.verified = False

                results.append(tweet)

                if tweetObject.maxTweets > 0 and len(results) >= tweetObject.maxTweets:
                    active = False
                    break

        return results








