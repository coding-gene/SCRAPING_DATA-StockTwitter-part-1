import requests
from bs4 import BeautifulSoup
import pandas as pd

_stock_list = []

class ScrapeStockData:


    def __init__(self, env):
        self.url = env.get('url')

    def get_page_content(self):
        url = self.url
        headers = {'Cache-Control': 'no-cache'}
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        stock = \
            {
            'price': soup.find('div', {'class': 'D(ib) Mend(20px)'}).
                find_all('fin-streamer')[0]['value'],
            'changeNum': soup.find('div', {'class': 'D(ib) Mend(20px)'}).
                find_all('fin-streamer')[1].
                find('span', {'class': 'C($negativeColor)'}).text,
            'changePer': soup.find('div', {'class': 'D(ib) Mend(20px)'}).
                find_all('fin-streamer')[2].
                find('span', {'class': 'C($negativeColor)'}).text.replace('%)', '').replace('(', ''),
            }
        _stock_list.append(stock)

        return _stock_list

    def get_df(self, stock):
        df = pd.DataFrame(stock)

        return df

