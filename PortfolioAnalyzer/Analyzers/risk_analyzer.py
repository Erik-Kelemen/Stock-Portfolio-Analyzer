import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..analyzer import Analyzer
from . import nav_analyzer
import statsmodels.api as sm
from sklearn.metrics import r2_score

class Risk_Analyzer(Analyzer):
    """
    An analyzer for computing portfolio volatility, return, alpha, beta, sharpe, OLS regression + R-squared.
    """
    def __init__(self, trades, prices, dummy_trades):
        """
        Creates a dummy_trades DataFrame to use as the benchmark portfolio, by mirroring the cash flows
        of the user portfolio, but only to buy the S&P 500 (including fractional shares).
        """
        super().__init__(trades, prices)
        self.user_portfolio = nav_analyzer.NAV_Analyzer(trades, prices)
        self.SnP_portfolio = nav_analyzer.NAV_Analyzer(dummy_trades, prices)
        
        self.user_portfolio.analyze()
        self.SnP_portfolio.analyze()

        self.portfolios = {"User Portfolio" : self.user_portfolio,
                           "S&P 500 Portfolio": self.SnP_portfolio}
        
        self.stats = {'Portfolio' : [],
                      'Daily Volatility': [],
                      'Annualized Volatility': [],
                      'Daily Return': [],
                      'Annualized Return': [],
                      'Cumulative Return': [],
                      '90% VaR': [],
                      '95% VaR': [],
                      '99% VaR': []}
        
        self.metrics = {'Alpha': [],
                       'Beta': [],
                      'Sharpe': []}
        

    def analyze(self):
        """
        Computes stats for both the user and dummy portfolio separately for side by side comparison.
        Also computes alpha, beta, and sharpe, and performs OLS regression and 90%, 95%, 99% Value at Risk.
        """
        dly_returns = {}
        def annualize_return(dly_ret):
            return (1 + dly_ret / 100) ** 252 - 1
        
        for name, portf in self.portfolios.items():
            self.stats['Portfolio'].append(name)

            nav = portf.NAV_by_date.reset_index().rename(columns = {'date': 'date', 0: 'NAV'})
            
            nav['Daily Return'] = nav['NAV'].pct_change()
            
            nav['Cumulative Return'] = (1 + nav['Daily Return']).cumprod() - 1
            dly_returns[name] = nav['Daily Return']
            dly_volat = nav['Daily Return'].std()
            ann_volat = dly_volat * (252 ** 0.5)
            
            dly_ret = nav['Daily Return'].mean()
            ann_ret = annualize_return(dly_ret)

            portfolio_investment = portf.Cash_Holdings.max()
            
            VaR_90 = nav['Daily Return'].quantile(0.1) * portfolio_investment
            VaR_95 = nav['Daily Return'].quantile(0.05) * portfolio_investment
            VaR_99 = nav['Daily Return'].quantile(0.01) * portfolio_investment


            self.stats['Daily Volatility'].append(dly_volat)
            self.stats['Annualized Volatility'].append(ann_volat)
            self.stats['Daily Return'].append(dly_ret)
            self.stats['Annualized Return'].append(ann_ret)
            self.stats['Cumulative Return'].append(nav['Cumulative Return'].iloc[-1])
            self.stats['90% VaR'].append(VaR_90)
            self.stats['95% VaR'].append(VaR_95)
            self.stats['99% VaR'].append(VaR_99)
            
        
        portfolio_daily_returns = dly_returns["User Portfolio"].drop(0)
        benchmark_daily_returns = dly_returns["S&P 500 Portfolio"].drop(0)
        
        covariance = portfolio_daily_returns.cov(benchmark_daily_returns)
        variance = benchmark_daily_returns.var()
        beta = covariance / variance

        portfolio_average_return = portfolio_daily_returns.mean()
        benchmark_average_return = benchmark_daily_returns.mean()
        alpha = portfolio_average_return - (self.risk_free_rate + beta * (benchmark_average_return - self.risk_free_rate))

        portfolio_volatility = portfolio_daily_returns.std()
        sharpe_ratio = (portfolio_average_return - self.risk_free_rate) / portfolio_volatility
        
        X = sm.add_constant(benchmark_daily_returns)
        self.regression_model = sm.OLS(portfolio_daily_returns, X).fit()
        
        r_squared = self.regression_model.rsquared

        self.metrics = pd.DataFrame({
            'Alpha': [alpha],
            'Beta': [beta],
            'Sharpe Ratio': [sharpe_ratio],
            'R-squared': [r_squared],
            'Risk Free Rate': [self.risk_free_rate]
        })

    def display(self):
        st.markdown("### 3. Risk Analysis")
        st.write("""Risk analysis generated from comparing to a dummy portfolio of buying S&P 500 shares
                 in cash investments equal to the cash flows of the user portfolio. For example, if the user's
                 portfolio bought \$1000 worth of stocks on day 1 and \$500 worth of stocks on day 2, the 
                 dummy portfolio would buy shares equivalent to \$1000 of S&P 500 on day 1 and \$500 of 
                 S&P 500 on day 2. This helps get the best comparison of performance given the cash amounts invested.  
                 This analysis also includes portfolio volatility (daily and annualized), alpha, beta, and sharpe ratio.
                 A daily volatility of 0.5 means that, on average, the PnL of your portfolio is 
                 projected to rise/fall 0.5% per day. An annualized volatility of 8.5% means that,
                 on average, your PnL is expected to change by 8.5% per year.  
                 Lastly, it includes Value at Risk (VaR), which represents the level of losses expected to be
                 exceeded with a certain probability (1 - confidence level). For example, at 99% VaR, it represents
                 the level of loss expected to be exceeded with a probability of 1%.
                """)
        self.metrics = self.metrics.T.rename(columns={0: 'Value'})
        
        stats = pd.DataFrame(self.stats)
        stats.set_index('Portfolio')
        stats = stats.T
        stats = stats.set_axis(stats.iloc[0], axis=1)[1:]
        
        st.write(self.metrics)
        st.write(stats)
        st.write(self.regression_model.summary())
        

    def print(self):
        for stat, val in self.stats:
            st.write(stat, val)
    