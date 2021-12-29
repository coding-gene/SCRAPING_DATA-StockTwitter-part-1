from logic.twitter import ScrapeTwitterData
from logic.stock import ScrapeStockData
from logic.spark import PySpark
from logic.config import get_environment_variables
import logging
import time

from logic.yfinance import ScrapeYahooFinanceData


try:
    pocetak = time.time()
    logging.basicConfig(filename='logs.txt',
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f'Pocetak izvrsavanja zadatka.')

    envVar = get_environment_variables()
    #twitter = ScrapeTwitterData(envVar.get('twitter'))
    #stock = ScrapeStockData(envVar.get('stock'))
    # Twitter data
    #twitter_content = twitter.get_twitter_posts()
    #df_twitter = twitter.get_df(twitter_content)
    # Stock data
    #stock_content = stock.get_page_content()
    #print(stock_content)
    #df_stock = stock.get_df(stock_content)
    #print(df_stock)

    finance = ScrapeYahooFinanceData()
    gme = finance.get_gme_stock_data()
    yfinance = gme.to_csv('yfinance.csv', sep='\t', encoding='utf-8')
    print(gme)

    pyspark = PySpark()
    test = pyspark.test_pyspark()



except Exception:
    logging.exception(f'Dogodila se greska sljedeceg sadrzaja:')
    #pg.rollback_connections()
else:
    #pg.commit_connections()
    logging.info('Uspjesno izvrsen zadatak.')
finally:
    #pg.closing_connections()
    logging.info(f'Obrada trajala: {time.strftime("%H sati, %M minuta i %S sekundi.", time.gmtime(time.time() - pocetak))}\n')
    #logging.info('\n')