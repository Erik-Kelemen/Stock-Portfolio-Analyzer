import pandas as pd
import os
import sqlite3
import sys
sys.path.append('..')
import csv
import constants
import web_scraper

class DBManager:
    def instantiate_db_tables():
        """
        Create the required database tables if they do not already exist
        """
        print("Initializing database...\n")
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

        print("Initialized database successfully in {constants.\n")

        conn.commit()
        conn.close()

    def insert_prices(file_name, dataframe, load_from_df = False):
        """
        Load prices from a csv file and insert them into the database
        Returns the number of rows inserted
        """
        conn = sqlite3.connect(constants.DB_FILE)
        cursor = conn.cursor()
        if load_from_df:
            
        else:
            with open(file_name) as file:
                reader = csv.reader(file)
                next(reader)
                rows = list(reader)
        print(rows) 
        converted_rows = list(map(lambda row: [
            datetime.strptime(row[0], '%Y-%m-%d %H:%M').date().isoformat(),
            datetime.strptime(row[0], '%Y-%m-%d %H:%M').time().isoformat()] 
            + row[1:], rows))
        
        cursor.executemany("""INSERT INTO prices (date, ticker, price, currency)
                                VALUES(?, ?, ?, ?, ?, ?)""", converted_rows)

        conn.commit()
        conn.close()
        return cursor.rowcount
        
    def insert_trades(file_name):
        """
        Load trades from a csv file and insert them into the database
        Returns the number of rows inserted
        """
        conn = sqlite3.connect(constants.DB_FILE)
        cursor = conn.cursor()
        with open(file_name) as file:
            reader = csv.reader(file)
            next(reader)
            rows = list(reader)
            
        cursor.executemany("""INSERT INTO trades (date, ticker, qty)
                                VALUES(?, ?, ?, ?)""", rows)

        conn.commit()
        conn.close()
        print(f"Inserted {cursor.rowcount} trades\n")
        return cursor.rowcount

def load_prices():
    """
    Returns a DataFrame of all stock prices for the portfolio
    """
    conn = sqlite3.connect(constants.DB_FILE)
    df = pd.read_sql_query("SELECT * FROM prices", conn)
    conn.close()
    return df

def load_trades():
    """
    Returns a DataFrame of trades
    """
    conn = sqlite3.connect(constants.DB_FILE)
    df = pd.read_sql_query("SELECT * FROM trades", conn)
    conn.close()
    return df

def scrape_if_missing(trades):
    """
    Calls the web scraper to find the remaining stock tickers we are missing from the trades data.
    """
    unique_tickers = trades['ticker'].unique()
    print(type(unique_tickers))
    current_prices = load_prices()
    missing_tickers = set(unique_tickers) - set(current_prices['ticker'])
    remaining_data = web_scraper.load_prices(missing_tickers, start_date, end_date, current_prices)
    
if __name__ == "__main__":
    dbm = DBManager()
    dbm.instantiate_db_tables()
    dbm.insert_trades(constants.TRADES_FILE)
    
    trades = load_trades()
    prices = scrape_if_missing(trades)
    
    insert_prices()
    generate_prices()
    
