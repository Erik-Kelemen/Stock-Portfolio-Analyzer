import pandas as pd
import sqlite3
import csv
import constants
import datetime
from Accessor import web_scraper
import streamlit as st

class DBManager:
    
    def __init__(self):
        """
        Create the required database tables if they do not already exist
        """
        self.trades = None
        st.write("Initializing prices database...")
        conn = sqlite3.connect(constants.DB_FILE)
        
        conn.execute("""
            CREATE TABLE if not exists prices(
                    date date,
                    ticker varchar,
                    price real,
                    currency varchar,
                    CONSTRAINT unq UNIQUE (date, ticker))
            """)

        st.write(f"Initialized database successfully in {constants.DB_FILE}!\n")

        conn.commit()
        conn.close()
        self.read_trades()
        self.scrape_prices()
    
    def get_prices(self):
        """
        Returns a DataFrame of all stock prices for the portfolio
        """
        conn = sqlite3.connect(constants.DB_FILE)
        prices = pd.read_sql_query(f"SELECT * FROM prices", conn)
        conn.close()
        return prices
    
    def read_trades(self):
        """
        Load trades from a csv file and writes to a local pandas dataframe
        Returns the number of rows inserted
        """
        st.write(f"Importing trades from {constants.TRADES_FILE}")
        self.trades = pd.read_csv(constants.TRADES_FILE)
        st.write("Trades imported")
        return self.trades
    
    def get_trades(self):
        return self.trades
    
    def scrape_prices(self):
        """
        Load all missing prices using the web scraper.
        Returns the number of rows inserted.
        """
        st.write("Loading missing prices...")
        unique_tickers = self.trades['ticker'].unique()
        current_prices = self.get_prices()
        start_date, end_date = self.trades['date'].min(), self.trades['date'].max()
        rows = web_scraper.load_prices(unique_tickers, start_date, end_date, current_prices)
        conn = sqlite3.connect(constants.DB_FILE)
        cursor = conn.cursor()
        converted_rows = list(map(lambda row: [
            datetime.strptime(row[0], '%Y-%m-%d %H:%M').date().isoformat(),
            datetime.strptime(row[0], '%Y-%m-%d %H:%M').time().isoformat()] 
            + row[1:], rows))
        st.write("Inserting rows:")
        st.write(converted_rows)
        cursor.executemany("""INSERT INTO prices (date, ticker, price, currency)
                                VALUES(?, ?, ?, ?)""", rows)

        conn.commit()
        conn.close()
        return cursor.rowcount
    
  