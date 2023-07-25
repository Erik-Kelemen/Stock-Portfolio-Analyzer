import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..analyzer import Analyzer
from matplotlib.dates import MonthLocator, DateFormatter

class PNL_Analyzer(Analyzer):
    def __init__(self, trades, prices):
        super().__init__(trades, prices)
        self.anlyzd = False
        self.analyze()
        
    def analyze(self):
        if(not self.anlyzd):
            self.anlyzd = True
            self.interpolate_trades()

            # Merge prices and trades dataframes
            self.portfolio = pd.merge(self.prices, self.trades, on=['date', 'ticker'])
            # Calculate the net quantity of each ticker at each date
            self.portfolio['net_qty'] = self.portfolio.groupby(['ticker'])['qty'].cumsum()

            # Calculate the total value of each trade for each ticker/date
            self.portfolio['trade_value'] = self.portfolio['price_USD'] * self.portfolio['qty']

            # Calculate the realized PnL
            self.portfolio['realized_pnl'] = -self.portfolio.groupby(['ticker'])['trade_value'].cumsum().fillna(0)

            # Calculate the unrealized PnL for open positions
            self.portfolio['unrealized_pnl'] = self.portfolio['net_qty'] * self.portfolio['price_USD']

            # Combine the realized and unrealized PnL to get the total PnL
            self.portfolio['total_pnl'] = self.portfolio['realized_pnl'] + self.portfolio['unrealized_pnl']

            self.total_pnl = self.portfolio.groupby('date')['total_pnl'].sum().reset_index()
            self.realized_pnl = self.portfolio.groupby('date')['realized_pnl'].sum().reset_index()
            self.unrealized_pnl = self.portfolio.groupby('date')['unrealized_pnl'].sum().reset_index()

            self.total_pnl['date'] = pd.to_datetime(self.total_pnl['date'])
            self.total_pnl = self.total_pnl.set_index('date')['total_pnl']

            self.realized_pnl['date'] = pd.to_datetime(self.realized_pnl['date'])
            self.realized_pnl = self.realized_pnl.set_index('date')['realized_pnl']

            self.unrealized_pnl['date'] = pd.to_datetime(self.unrealized_pnl['date'])
            self.unrealized_pnl = self.unrealized_pnl.set_index('date')['unrealized_pnl']


    def display(self):
        st.markdown("### 2. Profits & Losses (PnL)")
        st.write("""Profits & Losses reflect the difference between total revenue generated (profits) and total 
                expenses incurred (losses) during that period. In this analyzer, it is treated by separating
                PnL into realized and unrealized profits & losses.
                """)
        plt.figure(figsize=(12, 7))
        plt.plot(self.total_pnl.index, self.total_pnl.values, marker='o', linestyle='-', markersize=5)
        
        months_locator = MonthLocator(interval=1)
        months_format = DateFormatter('%b %Y')
        plt.gca().xaxis.set_major_locator(months_locator)
        plt.gca().xaxis.set_major_formatter(months_format)
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('PnL')
        plt.title('Portfolio Profits & Losses across time')
        plt.tight_layout()
        st.pyplot(plt)
        
        plt.clf()
        
        plt.plot(self.unrealized_pnl.index, self.unrealized_pnl.values, marker = 'd', linestyle = '-', markersize=5, label = 'Unrealized PnL')
        plt.plot(self.realized_pnl.index, self.realized_pnl.values, marker = 's', linestyle = '-', markersize=5, label = 'Realized PnL')
        plt.gca().xaxis.set_major_locator(months_locator)
        plt.gca().xaxis.set_major_formatter(months_format)
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('PnL')
        plt.title('Portfolio Unrealized vs. Realized PnL across time')
        plt.tight_layout()
        st.pyplot(plt)

    def print(self):
        #super().print()
        st.write(self.portfolio)
        st.write(self.tot_pnl)
        st.write(self.realized_pnl)
        st.write(self.unrealized_pnl)