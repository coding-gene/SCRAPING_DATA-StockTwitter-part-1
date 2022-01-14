from textblob import TextBlob


class TwitterSentimentAnalysis:

    def __init__(self, data):
        self.df = data

    @staticmethod
    def subjectivity(tweet):
        return TextBlob(tweet).sentiment.subjectivity

    @staticmethod
    def polarity(tweet):
        return TextBlob(tweet).sentiment.polarity

    def return_final_data(self, subj, pola):
        self.df['subjectivity'] = self.df['tweet'].apply(subj)
        self.df['polarity'] = self.df['tweet'].apply(pola)
        return self.df
