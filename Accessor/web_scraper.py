import csv
import datetime
from datetime import datetime
import yfinance as yf
import random
import pandas as pd
import os
import constants
import streamlit as st

canadian_stocks = ["RY.TO", "SHOP.TO", "BNS.TO", "TD.TO", "ENB.TO", "CAD=X"]
market_holidays = set([datetime(2022, 1, 17), datetime(2022,2,21), datetime(2022,4,15), 
                            datetime(2022, 5, 30), datetime(2022, 6, 20), datetime(2022, 7, 4), 
                            datetime(2022,9,5), datetime(2022, 11, 24), datetime(2022, 11, 25), 
                            datetime(2022, 12, 26)])

def load_prices(tickers, start_date, end_date, prices):
    """
    Loads all data for tickers between start_date and end_date inclusive that are not in prices.
    """
    #TODO: maybe we want to download all data for the tickers in my time range first, and just & it with my values?
    #tho this puts more pressure on the Exchange API...
    st.write(f"Fetching tickers for these tickers between {start_date} and {end_date}: ")
    st.write(tickers)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    all_pairs = pd.MultiIndex.from_product([date_range, tickers], names=['date', 'ticker'])
    existing_pairs = pd.MultiIndex.from_frame(prices[['date', 'ticker']])    
    missing_pairs = all_pairs.difference(existing_pairs)
    st.write(missing_pairs)
    rows = []

    def is_trading_day(date):
        return date.weekday() < 5 and date not in market_holidays
    
    for current_date, ticker in missing_pairs:
        if is_trading_day(current_date): continue
        dt = datetime.combine(current_date.date(), datetime.strptime("09:00:00", '%H:%M:%S').time())
        try:
            st.write(f"Loading {ticker} {dt}")
            data = yf.download(ticker, start=dt, end=dt + datetime.timedelta(minutes=1), interval='1d')
            st.write(data)
        except Exception as e:
            print(f"No data available for {ticker} on {current_date.strftime('%Y-%m-%d')} - Skipping.")
            continue

        if not data.empty:
            price = round(data['Close'][0], 2)
            currency = 'USD' if ticker not in canadian_stocks else 'CAD'
            rows.append((current_date, ticker, price, currency))
    st.write("Scraped the following rows using yfinance:")
    st.write(rows)
    return rows

def load_SNP500_tickers():
    """
    Optional utility to scrape for the list of S&P 500 companies.
    """
    filepath = 'S&P_500_tickers.txt'

    if os.path.exists(filepath):
        st.write(f"Tickers file found, loading from {filepath}")
        with open(filepath, 'r') as file:
            all_tickers = [line.strip() for line in file]
    else:
        st.write(f"No tickers file found, web scraping and writing to {filepath}.")
        URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tickers = pd.read_html(URL)[0]
        all_tickers = tickers.Symbol.to_list()
        with open(filepath, 'w') as file:
            file.writelines('\n'.join(all_tickers))
    return all_tickers