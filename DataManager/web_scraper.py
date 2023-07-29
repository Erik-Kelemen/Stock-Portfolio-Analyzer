from datetime import datetime
import yfinance as yf
import pandas as pd
import os
import streamlit as st

canadian_stocks = ["RY.TO", "SHOP.TO", "BNS.TO", "TD.TO", "ENB.TO", "CAD=X"]


def load_prices(tickers, start_date, end_date):
    """
    Loads all data for tickers between start_date and end_date inclusive.
    Also loads the 3-month treasury bill (^IRX) to serve as the risk free rate.
    And lastly the S&P 500.
    """
    always_load = ["^TNX", "^GSPC"]
    tickers.extend([ticker for ticker in always_load if ticker not in tickers])
    if any([ticker.endswith(".TO") for ticker in tickers]) and "CAD=X" not in tickers:
        tickers.append("CAD=X")
    st.write(f"Fetching tickers for these tickers between {start_date} and {end_date}: ")
    st.write(tickers)
    df = yf.download(tickers, start_date, end_date)['Adj Close']
    st.write("Loaded from yfinance:")
    st.write(df)
    
    st.write("Performing linear interpolation on the nulls:")
    for ticker in tickers:
        df[ticker] = df[ticker].interpolate()
    st.write(df)
    
    st.write("Performing backfill for first row nulls (if any):")
    for col in df.columns:
        if pd.isna(df.iloc[0][col]):
            df[col] = df[col].fillna(df.iloc[1][col])
    st.write(df)

    return df

def load_risk_free_rate():
    pass

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