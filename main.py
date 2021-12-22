from logic.twitterScrape import ScrapeTwitterData
from logic.stockScrape import ScrapeStockData
from logic.config import get_environment_variables
import logging
import time


try:
    pocetak = time.time()
    logging.basicConfig(filename='logs.txt',
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('Početak izvršavanja zadatka.')

    envVar = get_environment_variables()
    #twitter = ScrapeTwitterData(envVar.get('twitter'))
    stock = ScrapeStockData(envVar.get('stock'))
    # Twitter data
    #twitter_content = twitter.get_twitter_posts()
    #df_twitter = twitter.get_df(twitter_content)
    # Stock data
    stock_content = stock.get_page_content()
    print(stock_content)
    df_stock = stock.get_df(stock_content)
    print(df_stock)


except Exception:
    logging.exception('Dogodila se greška sljedećeg sadržaja:')
    #pg.rollback_connections()
else:
    #pg.commit_connections()
    logging.info('Uspješno izvršen zadatak.')
finally:
    #pg.closing_connections()
    logging.info(f'Obrada trajala: {time.strftime("%H sati, %M minuta i %S sekundi.", time.gmtime(time.time() - pocetak))}\n')
    #logging.info('\n')