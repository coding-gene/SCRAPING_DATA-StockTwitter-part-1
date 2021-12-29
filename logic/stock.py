import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

_stock_list = []

class ScrapeStockData:


    def __init__(self, env):
        self.url = env.get('url')

    def get_page_content(self):
        url = self.url
        headers = {'Cache-Control': 'no-cache'}
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        timeout = 300
        timeout_start = time.time()
        while time.time() < timeout_start + timeout:
            stock = \
                {
                'price': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text,
                'changeNum': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'})[0].text,
                'changePer': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'})[1].text.replace('%)', '').replace('(', ''),
                }
            _stock_list.append(stock)
            time.sleep(2)

        return _stock_list

    def get_df(self, stock):
        df = pd.DataFrame(stock)

        return df