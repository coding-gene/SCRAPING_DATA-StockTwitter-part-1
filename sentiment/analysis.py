from textblob import TextBlob
import sqlite3


class TwitterSentimentAnalysis:

    def __init__(self, data):
        self.df = data
        self.__sqlite__()

    def __sqlite__(self):
        self.connection = sqlite3.connect('twitter.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS tweet_sentiment_analysis
            (scrape_datetime TEXT NOT NULL,
            tweet TEXT NOT NULL,
            tweet_datetime TEXT NOT NULL,
            tweet_id TEXT NOT NULL,
            author_id TEXT NOT NULL,
            author_name TEXT NOT NULL,
            author_screen_name TEXT NOT NULL,
            subjectivity TEXT NOT NULL,
            polarity TEXT NOT NULL,
            sentiment TEXT NOT NULL)
            """)
        self.connection.commit()

    @staticmethod
    def subjectivity(tweet):
        return TextBlob(tweet).sentiment.subjectivity

    @staticmethod
    def polarity(tweet):
        return TextBlob(tweet).sentiment.polarity

    @staticmethod
    def sentiment(polarity):
        if polarity < 0:
            return 'Negative'
        elif polarity == 0:
            return 'Neutral'
        else:
            return 'Positive'

    def return_final_data(self, subj, pola, sent):
        self.df['subjectivity'] = self.df['tweet'].apply(subj)
        self.df['polarity'] = self.df['tweet'].apply(pola)
        self.df['sentiment'] = self.df['polarity'].apply(sent)
        self.df = self.df.applymap(str)

        #  todo: postaviti df filter da uzima samo najsvjeziji tweet

        for index, row in self.df.iterrows():
            self.cursor.execute(
                "INSERT INTO tweet_sentiment_analysis ("
                "scrape_datetime, tweet, tweet_datetime, tweet_id, author_id, author_name, "
                "author_screen_name, subjectivity, polarity, sentiment)"
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                    row.scrape_datetime,
                    row.tweet,
                    row.tweet_datetime,
                    row.tweet_id,
                    row.author_id,
                    row.author_name,
                    row.author_screen_name,
                    row.subjectivity,
                    row.polarity,
                    row.sentiment))
            self.connection.commit()
