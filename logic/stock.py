import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import sqlite3


class ScrapeStockData:

    def __init__(self, env):
        self.url = env.get('url')
        self.__sqlite__()

    def __sqlite__(self):
        self.connection = sqlite3.connect('stock.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS gme_stock_data
            (date_time TEXT NOT NULL,
            price INTEGER,
            change_number INTEGER,
            change_percentage INTEGER)
            """)
        self.connection.commit()

    def save_page_content(self):
        url = self.url
        headers = {'Cache-Control': 'no-cache'}
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        # timeout = 10
        # timeout_start = time()
        # while time() < timeout_start + timeout:

        while True:
            price = soup.find('div', {'class': 'D(ib) Mend(20px)'}). \
                find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
            changeNum = soup.find('div', {'class': 'D(ib) Mend(20px)'}). \
                find_all('fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'})[0].text
            changePer = soup.find('div', {'class': 'D(ib) Mend(20px)'}). \
                find_all('fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'})[1].text.replace('%)', ''). \
                replace('(', '')

            self.cursor.execute(
                "INSERT INTO gme_stock_data (date_time, price, change_number, change_percentage) "
                "VALUES (?, ?, ?, ?)", (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), price, changeNum, changePer))
            self.connection.commit()
            sleep(1)

    def closing_connection(self):
        self.connection.close()

    def rollback_connection(self):
        self.connection.rollback()
