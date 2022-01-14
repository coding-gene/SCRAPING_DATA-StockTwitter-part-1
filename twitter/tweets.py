import tweepy
from textblob import TextBlob
import pandas as pd
from datetime import datetime


class ScrapeTwitterData:

    def __init__(self, env):
        self.APIKey = env.get('APIKey')
        self.APIKeySecret = env.get('APIKeySecret')
        self.AccessToken = env.get('AccessToken')
        self.AccessTokenSecret = env.get('AccessTokenSecret')
        self.BearerToken = env.get('BearerToken')
        self.__twitter_authentication__()

    def __twitter_authentication__(self):
        self.authentication = tweepy.OAuthHandler(self.APIKey, self.APIKeySecret)
        self.authentication.set_access_token(self.AccessToken, self.AccessTokenSecret)
        self.api = tweepy.API(self.authentication, wait_on_rate_limit=True)

    def get_twitter_posts(self):
        _list_of_tweets = []
        tweets = tweepy.Cursor(self.api.search_tweets, q='#GameStopstock', lang='en').items(10)
        for tweet in tweets:
            _dict = {}
            try:
                _dict['date_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                _dict['Tweets'] = tweet.text
            except:
                _dict['date_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                _dict['Tweets'] = None
            _list_of_tweets.append(_dict)

        return _list_of_tweets

    def get_df(self, tweets):
        df = pd.DataFrame(tweets)

        return df
