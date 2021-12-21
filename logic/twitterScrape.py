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
        self.__twitter_authentication__()

    def __twitter_authentication__(self):
        self.auth = tweepy.OAuthHandler(self.APIKey, self.APIKeySecret)
        self.auth.set_access_token(self.AccessToken, self.AccessTokenSecret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    def get_twitter_posts(self):
        #posts = tweepy.Cursor(self.api.search_tweets, q='space', lang='eng').items(20)
        for tweet in tweepy.Cursor(self.api.search, q='#bmw', rpp=100).items(10):
            return tweet
