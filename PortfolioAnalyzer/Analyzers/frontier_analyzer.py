import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..portfolio_analyzer import PortfolioAnalyzer

class Frontier_Analyzer(PortfolioAnalyzer):
    def analyze(self):
        st.write("6. Efficient Frontier Analyzer")
        
        pass
    def graph(self):
        st.write("Efficient Frontier:")
        pass

def efficient_frontier(self):
        portfolio_returns = np.dot(self.trades, self.profits_losses)
        portfolio_volatility = np.std(portfolio_returns)
        
        min_volatility = np.min(portfolio_volatility)
        max_volatility = np.max(portfolio_volatility)
        step_size = (max_volatility - min_volatility) / 100
        
        frontier_returns = []
        frontier_volatility = []
        
        for volatility in np.arange(min_volatility, max_volatility, step_size):
            mask = portfolio_volatility <= volatility
            returns = portfolio_returns[mask]
            frontier_returns.append(np.mean(returns))
            frontier_volatility.append(volatility)