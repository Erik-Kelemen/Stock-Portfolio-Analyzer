import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..portfolio_analyzer import PortfolioAnalyzer

class Variance_Analyzer(PortfolioAnalyzer):
    def analyze(self):
        st.write("6.Variance Analyzer")
        
        pass
    def graph(self):
        st.write("Portfolio Variance across time:")
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