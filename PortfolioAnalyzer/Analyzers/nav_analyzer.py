import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
from ..analyzer import Analyzer
from datetime import datetime

class NAV_Analyzer(Analyzer):
    def __init__(self, trades, prices):
        super().__init__(trades, prices)
        self.anlyzd = False
        self.analyze()

    def analyze(self):
        """
        Computes the Net Asset Value (NAV) per day for the date range of trades.
        Also computes the Cash-Adjusted Net Asset Value, which is equivalent to P&L.
        """
        if(not self.anlyzd):
            self.anlyzd = True
            self.preprocess()
            self.holdings = self.trades.cumsum(axis = 0)

            self.NAV = self.prices * self.holdings
            self.NAV_by_ticker = self.NAV.sum(axis=0)
            self.NAV_by_date = self.NAV.sum(axis=1)
            self.NAV_by_date.index = pd.to_datetime(self.NAV_by_date.index)
            
            self.Cash_Flows = (self.prices * self.trades).sum(axis=1)
            self.Cash_Flows.index = pd.to_datetime(self.Cash_Flows.index)
            self.Cash_Holdings = self.Cash_Flows.cumsum()
            self.Cash_Adjusted_NAV = self.NAV_by_date - self.Cash_Holdings
            # self.print()
    
    def display(self):
        st.markdown("### 1. Net Asset Value (NAV)")
        st.write("""Net Asset Value is the current value of the portfolio, calculated as the SUM market value of 
                long positions - short positions. It is different from profits & losses, which include the cost
                of purchasing the particular investment.
                """)
        st.write(""" Assumptions:  
                1. Trades represent changes to the positions and are transferred into 
                the portfolio before the market open.   
                2. Portfolio NAV is assumed to be $0 prior to the first trade date.  
                """)
        st.write("Net Asset Value (NAV) across time:")
        plt.figure(figsize=(12, 8))
        
        plt.plot(self.NAV_by_date.index, self.NAV_by_date.values, marker='o', linestyle='-', markersize=5)

        months_locator = MonthLocator(interval=1)
        months_format = DateFormatter('%b %Y')
        plt.gca().xaxis.set_major_locator(months_locator)
        plt.gca().xaxis.set_major_formatter(months_format)

        plt.xlabel('Date')
        plt.ylabel('NAV')
        plt.title('Net Asset Value (NAV) Over Time')
        plt.tight_layout()
        st.pyplot(plt)
        plt.clf()
        st.write("Net Asset Value (NAV) by ticker:")
        plt.figure(figsize=(12, 8))
        plt.bar(self.NAV_by_ticker.index, self.NAV_by_ticker.values)

        plt.xlabel('Ticker')
        plt.ylabel('NAV')
        plt.title('Net Asset Value (NAV) by ticker')
        plt.tight_layout()
        st.pyplot(plt)

    def print(self):
        """
        For displaying backend dataframe to the user or debugging.
        """
        super().print()
        st.write(self.NAV)
        st.write(self.NAV_by_ticker)
        st.write(self.NAV_by_date)