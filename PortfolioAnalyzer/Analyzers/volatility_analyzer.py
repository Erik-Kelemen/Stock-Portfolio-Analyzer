import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..portfolio_analyzer import PortfolioAnalyzer
from matplotlib.dates import MonthLocator, DateFormatter

class Volatility_Analyzer(PortfolioAnalyzer):
    def __init__(self, trades, prices, nav_anlyzr, pnl_anlyzr):
        super().__init__(trades, prices)
        self.nav_anlyzr = nav_anlyzr
        self.pnl_analyzer = pnl_anlyzr

    def analyze(self):
        st.write("3. Volatility Analyzer")
        st.write(self.pnl_analyzer.tot_pnl)
        st.write(self.nav_anlyzr.NAV_by_date)
        
        self.PnL_daily_volatility = self.pnl_analyzer.daily_returns.std()
        self.PnL_annualized_volatility = self.PnL_daily_volatility * (252 ** 0.5)

        self.NAV_daily_volatility = self.NAV_analyzer.NAV_daily_returns.std()
        self.NAV_annualized_volatility = self.NAV_daily_volatility * (252 ** 0.5)
        pass
    def display(self):
        st.markdown("### 3. Volatility")
        st.write("""Volatility is a measure of portfolio risk. Smaller volatilities are associated with
                more stable portfolios. In this analysis we will show both daily and annualized volatilities
                for both PnL and NAV.
                """)
        plt.figure(figsize=(12, 7))
        plt.plot(self.tot_pnl.index, self.tot_pnl.values, marker='o', linestyle='-', markersize=5)
        
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
        # st.write("Portfolio Volatility across time:")
        pass

class RiskAnalyzer:
    def __init__(self, stock_prices, trades, profits_losses):
        self.stock_prices = stock_prices
        self.trades = trades
        self.profits_losses = profits_losses
    
    def calculate_variance(self, confidence_level=0.95):
        portfolio_returns = np.dot(self.trades, self.profits_losses)
        portfolio_returns.sort_values(inplace=True)
        var_index = int((1 - confidence_level) * len(portfolio_returns))
        var = portfolio_returns.iloc[var_index]
        return var