import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..analyzer import Analyzer
from . import nav_analyzer

class Risk_Analyzer(Analyzer):
    def __init__(self, trades, prices, nav_anlyzr = None):
        super().__init__(trades, prices)
        
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
        dates = nav_anlyzr.Cash_Flows.reset_index()['date']
        
        self.dummy_prices = prices[(pd.to_datetime(prices['date']).isin(dates) & (prices['ticker'] == '^GSPC'))][['date', 'price_USD']]
        self.dummy_prices['date'] = pd.to_datetime(self.dummy_prices['date'])
        self.dummy_prices = self.dummy_prices.set_index('date').iloc[:, 0]
        
        self.dummy_trades = nav_anlyzr.Cash_Flows / self.dummy_prices
        
        self.dummy_trades = pd.DataFrame({"date": dates,
                                     "ticker": ["^GSPC"] * len(dates),
                                     "qty": self.dummy_trades.tolist()})
        self.SnP_portfolio = nav_analyzer.NAV_Analyzer(self.dummy_trades, self.prices)
        self.user_portfolio = nav_anlyzr
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

            nav = portf.NAV_by_date.reset_index().rename(columns = {'date': 'date', 0: 'NAV'})
            
            nav['daily_returns'] = nav['NAV'].pct_change()
            
            nav['cumulative_returns'] = (1 + nav['daily_returns']).cumprod() - 1
            dly_returns[name] = nav['daily_returns']
            dly_volat = nav['daily_returns'].std()
            ann_volat = dly_volat * (252 ** 0.5)
            
            dly_ret = nav['daily_returns'].mean()
            ann_ret = annualize_return(dly_ret)

            portfolio_investment = portf.Cash_Holdings.max()
            
            VaR_90 = nav['daily_returns'].quantile(0.1) * portfolio_investment
            VaR_95 = nav['daily_returns'].quantile(0.05) * portfolio_investment
            VaR_99 = nav['daily_returns'].quantile(0.01) * portfolio_investment

            self.stats['Daily Volatility'].append(dly_volat)
            self.stats['Annualized Volatility'].append(ann_volat)
            self.stats['Daily Return'].append(dly_ret)
            self.stats['Annualized Return'].append(ann_ret)
            self.stats['Cumulative Return'].append(nav['cumulative_returns'].iloc[-1])
            self.stats['90% VaR'].append(VaR_90)
            self.stats['95% VaR'].append(VaR_95)
            self.stats['99% VaR'].append(VaR_99)

        risk_free_rate = self.prices[self.prices['ticker'] == '^TNX']['price'].iloc[0] / 100
        
        # Assuming you have daily returns of your portfolio and the benchmark index
        portfolio_daily_returns = dly_returns["User Portfolio"]
        benchmark_daily_returns = dly_returns["S&P 500 Portfolio"] 
        
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
        st.write("""Risk analysis generated from comparing to a dummy portfolio of buying S&P 500 shares
                 in cash investments equal to the cash flows of the user portfolio. For example, if the user's
                 portfolio bought \$1000 worth of stocks on day 1 and \$500 worth of stocks on day 2, the 
                 dummy portfolio would buy shares equivalent to \$1000 of S&P 500 on day 1 and \$500 of 
                 S&P 500 on day 2. This helps get the best comparison of performance given the cash amounts invested.  
                 This analysis also includes portfolio volatility (daily and annualized), alpha, beta, and sharpe ratio.
                 A daily volatility of 0.5 means that, on average, the PnL of your portfolio is 
                 projected to rise/fall 0.5% per day. An annualized volatility of 8.5% means that,
                 on average, your PnL is expected to change by 8.5% per day.  
                 Lastly, it includes Value at Risk (VaR), which represents the level of losses expected to be
                 exceeded with a certain probability (1 - confidence level). For example, at 99% VaR, it represents
                 the level of loss expected to be exceeded with a probability of 1%.
                """)
        self.metrics = self.metrics.T.rename(columns={0: 'Value'})
        st.write(self.metrics)
        df = pd.DataFrame(self.stats)
        df.set_index('Portfolio')
        df = df.T
        df = df.set_axis(df.iloc[0], axis=1)[1:]
        st.write(df)
        
    def print(self):
        for stat, val in self.stats:
            st.write(stat, val)
    