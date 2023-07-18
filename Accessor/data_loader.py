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
        st.write("Initializing database...")
        conn = sqlite3.connect(constants.DB_FILE)

        conn.execute("""
            CREATE TABLE if not exists trades(
                    date date,
                    ticker varchar,
                    qty real)
            """)

        conn.execute("""
            CREATE TABLE if not exists prices(
                    date date,
                    ticker varchar,
                    price real,
                    currency varchar)
            """)

        st.write(f"Initialized database successfully in {constants.DB_FILE}!\n")

        conn.commit()
        conn.close()
    
    def read_csv(self, file_name):
        with open(file_name) as file:
            reader = csv.reader(file)
            next(reader)
            rows = list(reader)
        return rows
        
    def insert_trades(self):
        """
        Load trades from a csv file and insert them into the database
        Returns the number of rows inserted
        """
        rows = self.read_csv(constants.TRADES_FILE)
        conn = sqlite3.connect(constants.DB_FILE)
        cursor = conn.cursor()
            
        cursor.executemany("""INSERT INTO trades (date, ticker, qty)
                                VALUES(?, ?, ?)""", rows)

        conn.commit()
        conn.close()
        print(f"Inserted {cursor.rowcount} trades\n")
        return cursor.rowcount
    
    def insert_prices(self):
        """
        Load prices from a csv file and insert them into the database
        Returns the number of rows inserted
        """
        # rows = self.read_csv(constants.PRICES_FILE)
        
        conn = sqlite3.connect(constants.DB_FILE)
        cursor = conn.cursor()
        converted_rows = list(map(lambda row: [
            datetime.strptime(row[0], '%Y-%m-%d %H:%M').date().isoformat(),
            datetime.strptime(row[0], '%Y-%m-%d %H:%M').time().isoformat()] 
            + row[1:], rows))
        
        cursor.executemany("""INSERT INTO prices (date, ticker, price, currency)
                                VALUES(?, ?, ?, ?)""", converted_rows)

        conn.commit()
        conn.close()
        return cursor.rowcount
    
    def get_table(self, table_name):
        conn = sqlite3.connect(constants.DB_FILE)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    
    def get_prices(self):
        """
        Returns a DataFrame of all stock prices for the portfolio
        """
        return self.get_table("prices")

    def get_trades(self):
        """
        Returns a DataFrame of the trades, read from the db.
        """
        return self.get_table("trades")
    
    def scrape_if_missing(self, trades):
        """
        Calls the web scraper to find the remaining stock tickers we are missing from the trades data.
        """
        unique_tickers = trades['ticker'].unique()
        print(type(unique_tickers))
        current_prices = self.get_prices()
        # missing_tickers = set(unique_tickers) - set(current_prices['ticker'])
        start_date, end_date = trades['date'].min(), trades['date'].max()
        remaining_data = web_scraper.load_prices(unique_tickers, start_date, end_date, current_prices)
