import streamlit as st
import pandas as pd
import numpy as np

class PortfolioAnalyzer:
    def __init__(self, trades, prices):
        self.trades = trades
        self.prices = prices
    def preprocess(self):
        """
        A preprocessing function for fitting the dimensions of prices and trades to each other,
        accounting for null dates and filtering out all tickers from prices which aren't in trades.
        """
        # Transform into dates * tickers, where each cell is a price or quantity
        self.prices = self.prices.pivot(index = 'date', columns = 'ticker', values = 'price_USD')
        self.trades = self.trades.pivot(index = 'date', columns = 'ticker', values = 'qty').fillna(0)
        
        # Drop all price columns not in trades and reindex to align columns
        common_columns = self.prices.columns.intersection(self.trades.columns)
        self.prices = self.prices[common_columns].reindex(columns = self.trades.columns)
        self.trades = self.trades.reindex(self.prices.index, fill_value = 0)

    def prefix_sum_trades(self):
        # Prefix sum down the columns to get net trades at each point in time, not deltas:
        self.trades = self.trades.cumsum(axis = 0)

        
    def print(self):
        st.write(f"{self.prices.shape[0]} x {self.prices.shape[1]}")
        st.write(self.prices)
        st.write(f"{self.trades.shape[0]} x {self.trades.shape[1]}")
        st.write(self.trades)

    def analyze(self):
        pass
    def display(self):
        pass