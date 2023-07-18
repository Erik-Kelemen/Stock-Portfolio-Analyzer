import pandas as pd
import numpy as np

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