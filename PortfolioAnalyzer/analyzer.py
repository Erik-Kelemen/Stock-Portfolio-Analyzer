import streamlit as st
import pandas as pd
import numpy as np

class Analyzer:
    def __init__(self, trades, prices):
        """
        Initialize the trades and prices dataframes to the analyzer.
        Also backs up the risk free rate as a decimal, computed as the ten year treasury bond on day 1 of trades.
        """
        self.trades = trades
        self.prices = prices
        self.risk_free_rate = self.prices[self.prices['ticker'] == '^TNX']['price'].iloc[0] / 100
    
    def create_dummy_trades(self):
        """
        Use on a dummy analyzer to create and return the dummy trades dataframe.
        """
        bcp_prices = self.prices.copy()
        self.preprocess()
        Cash_Flows = (self.prices * self.trades).sum(axis=1)
        dates = Cash_Flows.index

        dummy_prices = bcp_prices[(bcp_prices['date'].isin(dates) & (bcp_prices['ticker'] == '^GSPC'))][['date', 'price_USD']]
        dummy_prices = dummy_prices.set_index('date').iloc[:, 0]
        dummy_trades = Cash_Flows / dummy_prices

        dummy_trades = pd.DataFrame({"date": dates.tolist(),
                                        "ticker": ["^GSPC"] * len(dates),
                                        "qty": dummy_trades.tolist()}) 
        return dummy_trades
    
    def preprocess(self):
        """
        A preprocessing function for fitting the dimensions of prices and trades to each other,
        accounting for null dates and filtering out all tickers from prices which aren't in trades.
        """
        self.prices = self.prices.pivot(index = 'date', columns = 'ticker', values = 'price_USD')
        self.trades = self.trades.pivot(index = 'date', columns = 'ticker', values = 'qty').fillna(0)
        
        common_columns = self.prices.columns.intersection(self.trades.columns)
        self.prices = self.prices[common_columns].reindex(columns = self.trades.columns)
        self.trades = self.trades.reindex(self.prices.index, fill_value = 0)
    
    def interpolate_trades(self):
        """
        Fills self.trades with qty = 0 for days where no trades are made to that ticker.
        """
        unique_dates = self.trades['date'].unique()

        all_tickers = self.trades['ticker'].unique()
        all_combinations = pd.MultiIndex.from_product([unique_dates, all_tickers], names=['date', 'ticker'])
        all_trades = pd.DataFrame(index=all_combinations).reset_index()

        self.trades = pd.merge(all_trades, self.trades, on=['date', 'ticker'], how='left').fillna(0)
        
    def print(self):
        """
        Pretty print the state of the analyzer. Primarily for debugging.
        """
        st.write(f"{self.prices.shape[0]} x {self.prices.shape[1]}")
        st.write(self.prices)
        st.write(f"{self.trades.shape[0]} x {self.trades.shape[1]}")
        st.write(self.trades)

    def analyze(self):
        """
        Primary analyzer to override.
        """
        pass
    def display(self, dummy = None):
        """
        Primary display function to override. Runs after the analyzer in the controller.py."""
        pass