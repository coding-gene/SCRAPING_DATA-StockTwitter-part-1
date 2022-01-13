# from logic.twitter import ScrapeTwitterData
from logic.stock import ScrapeStockData
from logic.config import get_env_variables
import logging
import time

start_time = time.time()
logging.basicConfig(filename='logs.txt',
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.info('Job started.')
# noinspection PyBroadException
try:
    eVar = get_env_variables()
    # twitter = ScrapeTwitterData(eVar.get('twitter'))
    stock = ScrapeStockData(eVar.get('stock'))

    # Twitter data
    # twitter_content = twitter.get_twitter_posts()
    # df_twitter = twitter.get_df(twitter_content)

    # Stock data
    stock_content = stock.save_page_content()
except Exception:
    logging.exception('An error occurred during job performing:')
    stock.rollback_connection()
else:
    logging.info('Job ended.')
finally:
    stock.closing_connection()
    logging.info(
        f'Job duration: {time.strftime("%H hours, %M minutes, %S seconds.", time.gmtime(time.time() - start_time))}\n')
