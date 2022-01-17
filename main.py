# https://codeofaninja.com/tools/find-twitter-id/
# https://blog.jovian.ai/stock-sentiment-analysis-and-summarization-via-web-scraping-6ae9a115c8c8
from configuration.environment import environment_variables
from twitter.tweets import ScrapeTwitterData
from stock.gamestop import ScrapeStockData
from sentiment.analysis import TwitterSentimentAnalysis
import logging
import time
import pandas as pd

pd.set_option('display.max_rows', 40)
pd.set_option('display.max_columns', 40)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 300)

start_time = time.time()
logging.basicConfig(filename='logs.txt',
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.info('Job started.')
# noinspection PyBroadException
try:
    eVar = environment_variables()
    twitter = ScrapeTwitterData(eVar.get('twitter'))
    stock = ScrapeStockData(eVar.get('stock'))

    #  specify time of loop working or take infinite while loop
    #  timeout = 20
    #  timeout_start = time.time()
    #  while time.time() < timeout_start + timeout:
    while True:
        #  Stock data
        stock_content = stock.save_page_content()

        # Twitter data
        twitter_content = twitter.get_twitter_posts()
        df_tweets = twitter.get_df(twitter_content, twitter.clean_tweets)

        # Sentiment analysis
        sentiment = TwitterSentimentAnalysis(df_tweets)
        df_final = sentiment.return_final_data(
            sentiment.subjectivity,
            sentiment.polarity,
            sentiment.sentiment)
        time.sleep(5)
except Exception:
    logging.exception('An error occurred during job performing:')
    stock.rollback_connection()
    sentiment.rollback_connection()
finally:
    logging.info('Job ended.')
    stock.closing_connection()
    sentiment.closing_connection()
    logging.info(
        f'Job duration: {time.strftime("%H hours, %M minutes, %S seconds.", time.gmtime(time.time() - start_time))}\n')
