import pandas as pd
import numpy as np
from .Analyzers import nav_analyzer
from .Analyzers import pnl_analyzer
from .Analyzers import risk_analyzer
from .analyzer import Analyzer 
import streamlit as st

class Controller:
    def __init__(self, trades, prices):
        st.write(f"Welcome to the analyzer!")
        self.trades = trades
        self.prices = prices
        
        self.standardize_currency()

        benchmark_anlyzr = Analyzer(trades, prices)
        self.benchmark_trades = benchmark_anlyzr.create_dummy_trades()
        
        self.analyzers = [nav_analyzer.NAV_Analyzer,
                        pnl_analyzer.PNL_Analyzer,
                        risk_analyzer.Risk_Analyzer]
        
        
    def standardize_currency(self):
        """
        Standardize all stock prices to USD using the appropriate =X conversion rate in prices.
        Will drop the conversion rates from the prices table to eliminate pollution
        """
        st.write("Standarding all stock prices to USD:")
        if len(self.prices['currency'].unique()) > 1:
            date_to_rate = self.prices[(self.prices['ticker'] == 'CAD=X')].set_index(['date'])['price']
            def CAD_to_USD(date, currency, price):
                """
                Utility function for converting USD to CAD for a specific date and time.
                """
                return price if currency == 'USD' else price * (1 / date_to_rate[date])
            self.prices['price_USD'] = self.prices.apply(lambda row: 
                                            CAD_to_USD(row['date'], row['currency'], row['price']), 
                                            axis=1)
        else:
            st.write("All stock prices are already in USD.")
            
    def analyze(self):
        for analyzer in self.analyzers:
            if analyzer == risk_analyzer.Risk_Analyzer:
                anlyzr = analyzer(self.trades, self.prices, self.benchmark_trades)
                anlyzr.analyze()
                anlyzr.display()
            else:
                anlyzr = analyzer(self.trades, self.prices)
                benchmark_anlyzr = analyzer(self.benchmark_trades, self.prices)
                
                anlyzr.analyze()
                benchmark_anlyzr.analyze()

                anlyzr.display(benchmark_anlyzr)