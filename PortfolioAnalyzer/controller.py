import pandas as pd
import numpy as np
from .Analyzers import nav_analyzer
from .Analyzers import pnl_analyzer
from .Analyzers import alphas_analyzer
from .Analyzers import betas_analyzer
from .Analyzers import sharpes_analyzer
from .Analyzers import variance_analyzer
from .Analyzers import frontier_analyzer

import streamlit as st

class Controller:
    def __init__(self, trades, prices, analyzers = None):
        self.trades = trades
        self.prices = prices
        if not analyzers:
            analyzers = [nav_analyzer.NAV_Analyzer(trades, prices),
                         pnl_analyzer.PNL_Analyzer(trades, prices),
                         alphas_analyzer.Alphas_Analyzer(trades, prices),
                         betas_analyzer.Betas_Analyzer(trades, prices),
                         sharpes_analyzer.Sharpes_Analyzer(trades, prices),
                         variance_analyzer.Variance_Analyzer(trades, prices),
                         frontier_analyzer.Frontier_Analyzer(trades, prices)]
        self.analyzers = analyzers
        
        if len(self.prices['currency'].unique()) > 1:
            self.standardize() #convert all prices to USD
            
    def standardize(self):
        """
        Standardize all stock prices to USD using the appropriate =X conversion rate in prices.
        Will drop the conversion rates from the prices table to eliminate pollution
        """
        st.write("Standarding all stock prices to USD:")
        date_to_rate = self.prices[(self.prices['ticker'] == 'CAD=X')].set_index(['date'])['price']
        def CAD_to_USD(date, currency, price):
            """
            Utility function for converting USD to CAD for a specific date and time.
            """
            return price if currency == 'USD' else price * (1 / date_to_rate[date])
        self.prices['price_USD'] = self.prices.apply(lambda row: 
                                        CAD_to_USD(row['date'], row['currency'], row['price']), 
                                        axis=1)
        return self.prices
    def analyze(self):
        st.dataframe(self.prices)
        st.write("Welcome to the analyzer! All currencies are converted to USD.")
        for analyzer in self.analyzers:
            analyzer.analyze()
            analyzer.graph()