import tweepy
import pandas as pd
from datetime import datetime
import re
import emoji


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
        tweets = tweepy.Cursor(self.api.search_tweets, q='gmestock', type='recent', lang='en').items(20)
        for tweet in tweets:
            _dict = {}
            # noinspection PyBroadException
            try:
                _dict['scrape_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                _dict['tweet'] = tweet.text.lower()
                _dict['tweet_datetime'] = tweet.created_at
                _dict['tweet_id'] = tweet.id
                _dict['author_id'] = tweet.entities['user_mentions'][0]['id']
                _dict['author_name'] = tweet.entities['user_mentions'][0]['name'].lower()
                _dict['author_screen_name'] = tweet.entities['user_mentions'][0]['screen_name'].lower()
            except Exception:
                _dict['scrape_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                _dict['tweet'] = None
                _dict['tweet_datetime'] = None
                _dict['tweet_id'] = 0
                _dict['author_id'] = 0
                _dict['author_name'] = None
                _dict['author_screen_name'] = None
            _list_of_tweets.append(_dict)
        return _list_of_tweets

    @staticmethod
    def clean_tweets(tweet):
        tweet = re.sub(r'@[A-Za-z0-9_]+', '', tweet)  # mentions
        tweet = re.sub(r'#', '', tweet)  # hashtags r'#[A-Za-z0-9_]+'
        tweet = re.sub(r'http\S+', '', tweet)  # links
        tweet = re.sub(r'www.\S+', '', tweet)  # links
        tweet = re.sub(r'[()!?]', ' ', tweet)  # punctuations
        tweet = re.sub(r'\[.*?\]', ' ', tweet)  # punctuations
        tweet = re.sub(r'[^a-z0-9]', ' ', tweet)  # non-alphanumeric characters
        tweet = re.sub(r'rt[\s]+', '', tweet)  # rt
        tweet = re.sub(' +', ' ', tweet)  # multiple spaces
        tweet = ''.join(c for c in tweet if c not in emoji.UNICODE_EMOJI)  # emoji
        tweet = tweet.strip()  # strip spaces
        return tweet

    @staticmethod
    def get_df(tweets, func):
        df = pd.DataFrame(tweets)
        df['tweet_datetime'] = pd.to_datetime(df.tweet_datetime).dt.tz_localize(None)
        df = df[df.tweet_id != 0]
        df.drop_duplicates(subset='tweet', keep='first', inplace=True)
        df.reset_index(drop=True, inplace=True)

        df['tweet'] = df['tweet'].apply(func)
        df['author_name'] = df['author_name'].apply(func)

        return df
