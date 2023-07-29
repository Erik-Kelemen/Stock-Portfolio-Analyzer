import pandas as pd
import sqlite3
import constants
from DataManager import web_scraper
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class DBManager:
    
    def __init__(self):
        """
        Create the required database tables if they do not already exist
        """
        self.trades = None
        self.prices = None
        self.start_date, self.end_date = None, None
        conn = sqlite3.connect(constants.DB_FILE)
        
        conn.execute("""
            CREATE TABLE if not exists prices(
                    date date,
                    ticker varchar,
                    price real,
                    currency varchar,
                    CONSTRAINT unq UNIQUE (date, ticker))
            """)

        conn.commit()
        conn.close()
    
    def get_prices(self):
        """
        Returns a DataFrame of all stock prices for the portfolio
        """
        if self.prices is None:
            conn = sqlite3.connect(constants.DB_FILE)
            self.prices = pd.read_sql_query(f"SELECT * FROM prices", conn)
            conn.close()
            
        return self.prices
    
    def read_trades(self):
        """
        Load trades from a csv file and writes to a local pandas dataframe
        Returns the number of rows inserted
        """
        self.trades = pd.read_csv(constants.TRADES_FILE)
        st.write(f"Trades loaded:")
        return self.trades
    
    def get_trades(self):
        self.start_date, self.end_date = self.trades['date'].min(), self.trades['date'].max()
        return self.trades
    
    def scrape_prices(self):
        """
        Load all missing prices using the web scraper into the db.
        """
        # web_scraper.load_T_Bill_rate(self.start_date, self.end_date)
        st.write("Loading missing prices...")
        unique_tickers = self.trades['ticker'].unique()
        
        df = web_scraper.load_prices(unique_tickers.tolist(), self.start_date, self.end_date)
        conn = sqlite3.connect(constants.DB_FILE)
        cursor = conn.cursor()
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'date'}, inplace=True)
        df = df.melt(id_vars='Date', var_name='ticker', value_name='price')

        def get_currency(ticker):
            if ticker.endswith('TO'):
                return 'CAD'
            else:
                return 'USD'
        
        df['currency'] = df['ticker'].apply(get_currency)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        st.write("Persisting following rows to the database:")
        st.write(df)
        for _, row in df.iterrows():
            try:
                cursor.execute("INSERT INTO prices (date, ticker, price, currency) VALUES (?, ?, ?, ?)",
                            (row['Date'], row['ticker'], row['price'], row['currency']))
            except sqlite3.IntegrityError:
                pass
        conn.commit()
        conn.close()
    
    def graph_trades(self):
        plt.style.use('dark_background')
        color_map = []
        df = pd.DataFrame(self.trades)
        df['date'] = pd.to_datetime(df['date'])
        unique_tickers = df['ticker'].unique()

        color_map = {ticker: plt.cm.tab10(i) for i, ticker in enumerate(unique_tickers)}

        # Plot the graph
        plt.figure(figsize=(12, 7))
        for ticker, group in df.groupby('ticker'):
            plt.scatter(group['date'], group['qty'], color=color_map[ticker], label=ticker, s=10)

        # Add labels and title
        plt.xlabel('Date')
        plt.ylabel('Quantity')
        plt.title('Trades by Date (Color-coded by Ticker)')
        plt.legend(loc = 'upper right')

        # Show the legend (ticker key)
        st.pyplot(plt)
        plt.clf()
        for ticker, group in df.groupby('ticker'):
            plt.plot(group['date'], group['qty'], color=color_map[ticker], label=ticker)

        # Add labels and title
        plt.xlabel('Date')
        plt.ylabel('Quantity')
        plt.title('Trades by Date (Color-coded by Ticker)')
        plt.legend(loc = 'upper right')
        
        st.pyplot(plt)
    
    def graph_prices(self):
        
        ticker_colors = {ticker: f'C{i}' for i, ticker in enumerate(self.prices['ticker'].unique())}
        num_unique_tickers = len(ticker_colors)
        
        stocks = self.prices.loc[~self.prices['ticker'].isin(["^GSPC", "CAD=X", "^TNX"])]
        
        plt.figure(figsize=(12, 7))
        i = 0
        for ticker, group in stocks.groupby('ticker'):
            if ticker == '^GSPC': continue
            color = plt.cm.tab10(i % num_unique_tickers)
            plt.plot(pd.to_datetime(group['date']), group['price'], label=ticker, c=color)
            i += 1

        # Format the plot
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Stock Prices Across Time')
        plt.legend()
        
        ax = plt.gca()
        date_format = mdates.DateFormatter('%b %Y')
        ax.xaxis.set_major_formatter(date_format)

        # Set the x-axis locator to show 12 evenly spaced tick marks
        ax.xaxis.set_major_locator(mdates.MonthLocator())

        plt.tight_layout()
        st.pyplot(plt)

        