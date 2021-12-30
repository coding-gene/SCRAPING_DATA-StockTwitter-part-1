#from logic.twitter import ScrapeTwitterData
from logic.stock import ScrapeStockData
from logic.config import get_env_variables
import logging
import time

try:
    start_time = time.time()
    logging.basicConfig(filename='logs.txt',
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f'Pocetak izvrsavanja zadatka.')
    # Initializing local packages
    eVar = get_env_variables()
    #twitter = ScrapeTwitterData(eVar.get('twitter'))
    stock = ScrapeStockData(eVar.get('stock'))
    # Twitter data
    #twitter_content = twitter.get_twitter_posts()
    #df_twitter = twitter.get_df(twitter_content)
    # Stock data
    stock_content = stock.save_page_content()
except Exception:
    logging.exception(f'Dogodila se greska sljedeceg sadrzaja:')
    stock.rollback_connection()
else:
    logging.info('Uspjesno izvrsen zadatak.')
finally:
    stock.closing_connection()
    logging.info(f'Obrada trajala: {time.strftime("%H sati, %M minuta i %S sekundi.", time.gmtime(time.time() - start_time))}\n')