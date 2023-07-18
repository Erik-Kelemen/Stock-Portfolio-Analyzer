import pandas as pd
import numpy as np
from Accessor import data_loader
from PortfolioAnalyzer import portfolio_calc
from PortfolioAnalyzer import risk_analyzer
import streamlit as st

if __name__ == "__main__":
    prices = data_loader.load_prices();
    trades = data_loader.load_trades();
    print(prices.head())
    print(trades.head())
    portfolio_engine = portfolio_calc.PortfolioCalculator(prices, trades)
    NAV = portfolio_engine.nav()
    PnL = portfolio_engine.profits_and_losses()
    alphas = portfolio_engine.alphas()
    betas = portfolio_engine.betas()
    sharpes = portfolio_engine.sharpes()

    risk_analyzer = risk_analyzer.RiskAnalyzer(prices, trades, PnL)
    variance = risk_analyzer.calculate_variance()
    frontier = risk_analyzer.efficient_frontier()

    ui = interface.UI()
    data = {'NAV': NAV,
            'PnL': PnL,
            'alphas': alphas,
            'betas': betas,
            'sharpes': sharpes,
            'variance': variance,
            'frontier': frontier}
    ui.show(data)