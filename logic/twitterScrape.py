import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np


class ScrapeTwitterData:

    def __init__(self, env):
        self.APIKey = env.get('APIKey')
        self.APIKeySecret = env.get('APIKeySecret')
        self.AccessToken = env.get('AccessToken')
        self.AccessTokenSecret = env.get('AccessTokenSecret')
        self.BearerToken = env.get('BearerToken')
        self.__twitter_authentication__()

    def __twitter_authentication__(self):
        self.auth = tweepy.OAuthHandler(self.APIKey, self.APIKeySecret)
        self.auth.set_access_token(self.AccessToken, self.AccessTokenSecret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    """
    def __twitter_authentication__(self):
        self.client = tweepy.Client(bearer_token=self.BearerToken,
                                    consumer_key=self.APIKey,
                                    consumer_secret=self.APIKeySecret,
                                    access_token=self.AccessToken,
                                    access_token_secret=self.AccessTokenSecret)
    """

    def get_twitter_posts(self):
        _list_of_tweets = []
        tweets = tweepy.Cursor(self.api.search_tweets, q='#GameStopstock', lang='en').items(10)
        for tweet in tweets:
            _dict = {}
            try:
                _dict['Tweets'] = tweet.text
            except:
                _dict['Tweets'] = None
            _list_of_tweets.append(_dict)

        df = pd.DataFrame(_list_of_tweets)
        return df
