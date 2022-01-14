import tweepy
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
        #  self.client = tweepy.Client(bearer_token=self.BearerToken)

    def get_twitter_posts(self):
        _list_of_tweets = []
        tweets = tweepy.Cursor(self.api.search_tweets, q='#gmestock', type='recent', lang='en').items(6)
        for tweet in tweets:
            _dict = {}
            # noinspection PyBroadException
            try:
                _dict['scrape_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                _dict['tweet'] = tweet.text
                _dict['tweet_datetime'] = tweet.created_at
                _dict['tweet_id'] = tweet.id
                _dict['author_id'] = tweet.entities['user_mentions'][0]['id']
                _dict['author_name'] = tweet.entities['user_mentions'][0]['name']
            except Exception:
                _dict['scrape_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                _dict['tweet'] = None
                _dict['tweet_datetime'] = None
                _dict['tweet_id'] = 0
                _dict['author_id'] = 0
                _dict['author_name'] = None
            _list_of_tweets.append(_dict)
        return _list_of_tweets

    @staticmethod
    def get_df(tweets):
        df = pd.DataFrame(tweets)
        df['tweet_datetime'] = pd.to_datetime(df.tweet_datetime).dt.tz_localize(None)
        df = df[df.tweet_id != 0]
        df.reset_index()
        return df
