import yfinance as yf
import pandas as pd

class ScrapeYahooFinanceData:

    def __init__(self):
        self.stock_company = 'gme'

    def get_gme_stock_data(self):
        gme = yf.Ticker(self.stock_company)
        df = gme.history(period='5y')

        return df

