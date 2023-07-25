import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..analyzer import Analyzer
from . import pnl_analyzer

class Risk_Analyzer(Analyzer):
    def __init__(self, trades, prices, pnl_anlyzr):
        super().__init__(trades, prices)
        self.user_portfolio = pnl_anlyzr
        self.stats = {'Portfolio' : [],
                      'Daily Volatility': [],
                      'Annualized Volatility': [],
                      'Daily Return': [],
                      'Annualized Return': []}
        self.metrics = {'Alpha': [],
                       'Beta': [],
                      'Sharpe': []}
        dates = self.trades['date'].unique()
        self.dummy_trades = pd.DataFrame({"date": dates,
                                     "ticker": ["^GSPC"] * len(dates),
                                     "qty": [10] + [0] * (len(dates)-1)})
        self.SnP_portfolio = pnl_analyzer.PNL_Analyzer(self.dummy_trades, self.prices)
        self.portfolios = {"User Portfolio" : self.user_portfolio,
                           "S&P 500 Portfolio": self.SnP_portfolio}

    def analyze(self):
        """
        ^TNX --> 10-year U.S. treasury note
        ^GSPC --> S&P 500 Index
        Create dummy portfolio of holding 10 shares of S&P 500
        """
        dly_returns = {} 
        def annualize_return(dly_ret):
            return (1 + dly_ret / 100) ** 252 - 1
        
        for name, portf in self.portfolios.items():
            self.stats['Portfolio'].append(name)

            pnl = portf.total_pnl.reset_index()
            pnl.drop(0, inplace=True)
            pnl['daily_returns'] = pnl['total_pnl'].pct_change()
            
            dly_returns[name] = pnl['daily_returns']
            dly_volat = pnl['daily_returns'].std()
            ann_volat = dly_volat * (252 ** 0.5)
            
            dly_ret = pnl['daily_returns'].mean()
            ann_ret = annualize_return(dly_ret)

            self.stats['Daily Volatility'].append(dly_volat)
            self.stats['Annualized Volatility'].append(ann_volat)
            self.stats['Daily Return'].append(dly_ret)
            self.stats['Annualized Return'].append(ann_ret)
        
        risk_free_rate = self.prices[self.prices['ticker'] == '^TNX']['price'].iloc[0] / 100
        
        # Assuming you have daily returns of your portfolio and the benchmark index
        portfolio_daily_returns = dly_returns["User Portfolio"]
        benchmark_daily_returns = dly_returns["S&P 500 Portfolio"] 
        
        # Assuming you have the risk-free rate (annualized)
        risk_free_rate = 0.03

        # Calculate beta
        covariance = portfolio_daily_returns.cov(benchmark_daily_returns)
        variance = benchmark_daily_returns.var()
        beta = covariance / variance

        # Calculate alpha
        portfolio_average_return = portfolio_daily_returns.mean()
        benchmark_average_return = benchmark_daily_returns.mean()
        alpha = portfolio_average_return - (risk_free_rate + beta * (benchmark_average_return - risk_free_rate))

        # Calculate Sharpe ratio
        portfolio_volatility = portfolio_daily_returns.std()
        sharpe_ratio = (portfolio_average_return - risk_free_rate) / portfolio_volatility

        # Create a dataframe to store the results
        self.metrics = pd.DataFrame({
            'Alpha': [alpha],
            'Beta': [beta],
            'Sharpe Ratio': [sharpe_ratio]
        })

    def display(self):
        st.markdown("### 3. Risk Analysis")
        st.write("""Several portfolio summary metrics, including portfolio volatility 
                 (daily and annualized) from PnL, alpha, beta, and sharpe ratio.
                 A daily volatility of 0.5 means that, on average, the PnL of your portfolio is 
                 projected to rise/fall 0.5% per day. An annualized volatility of 8.5% means that,
                 on average, your PnL is expected to change by 8.5% per day.
                """)
        st.write(self.stats)
        st.write(self.metrics)
        df = pd.DataFrame(self.stats)
        st.write(list(df['Portfolio']))
        df = pd.melt(df, id_vars=list(df['Portfolio']))
        # df = df.pivot(index = columns = 'Portfolio')
        st.write(df)

    def print(self):
        for stat, val in self.stats:
            st.write(stat, val)
        
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