import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..portfolio_analyzer import PortfolioAnalyzer
from datetime import datetime
class NAV_Analyzer(PortfolioAnalyzer):
    def analyze(self):
        """
        Computes the Net Asset Value (NAV) per day for the date range of trades.
        Should return a Series with 1 value for each time bucket.
        """
        st.write("1. Net Asset Value (NAV)")
        st.write(""" Assumptions:
                1. Trades represent changes to the positions and are transferred into 
                the portfolio before the market open. 
                2. Portfolio NAV is the SUM market value of long positions – short positions.
                3. Portfolio NAV is assumed to be $0 prior to the first trade date.
                """)
        # Transform into dates * tickers, where each cell is a price or quantity
        self.prices = self.prices.pivot(index = 'date', columns = 'ticker', values = 'price_USD')
        self.trades = self.trades.pivot(index = 'date', columns = 'ticker', values = 'qty').fillna(0)
        
        # Drop all price columns not in trades and reindex to align columns
        common_columns = self.prices.columns.intersection(self.trades.columns)
        self.prices = self.prices[common_columns].reindex(columns = self.trades.columns)

        # Fill in missing dates in trades with 0's
        self.trades = self.trades.reindex(self.prices.index, fill_value = 0)

        # Prefix sum down the columns to get net trades, not deltas:
        self.trades = self.trades.cumsum(axis = 0)
        
        # st.write(f"{self.prices.shape[0]} x {self.prices.shape[1]}")
        # st.write(self.prices)
        # st.write(f"{self.trades.shape[0]} x {self.trades.shape[1]}")
        # st.write(self.trades)
        
        self.NAV = self.prices * self.trades
        # st.write(self.NAV)
        self.NAV_by_ticker = self.NAV.sum(axis=0)
        self.NAV_by_date = self.NAV.sum(axis=1)
        
    def graph(self):
        st.write("Net Asset Value (NAV) across time:")
        # st.write(self.NAV_by_date.columns)
        plt.figure(figsize=(10, 6))
        plt.plot(self.NAV_by_date.index, self.NAV_by_date.values, marker='o', linestyle='-', markersize=5)
        plt.xlabel('Date')
        plt.ylabel('NAV')
        plt.title('Net Asset Value (NAV) Over Time')
        # plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)


        st.write("Net Asset Value (NAV) by ticker:")
        # st.write(self.NAV_by_date.columns)
        plt.figure(figsize=(10, 6))
        plt.bar(self.NAV_by_ticker.index, self.NAV_by_ticker.values)
        plt.xlabel('Date')
        plt.ylabel('NAV')
        plt.title('Net Asset Value (NAV) by ticker')
        # plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)

    