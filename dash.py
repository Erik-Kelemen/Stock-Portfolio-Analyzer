import streamlit as st
import sys
import os
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import constants
from DataSource import generate_trades
from Accessor import data_loader
from PortfolioAnalyzer import controller

if(os.getcwd() not in sys.path):
    sys.path.append(os.getcwd())

# Header
st.title("Stock Portfolio Analyzer")
st.write("Welcome to the Stock Portfolio Analyzer! For any questions, refer to the README.md.")
st.write("Made by Erik Kelemen.")

trades_tab, prices_tab, analysis_tab = st.tabs(["Trades", "Prices", "Analysis"])

dbm = data_loader.DBManager()

# Dummy Trades
with trades_tab:
    def load_trades():
        dbm.read_trades()
        trades = dbm.get_trades()
        st.dataframe(trades)
        dbm.graph_trades()
    if not os.path.exists(constants.TRADES_FILE):
        st.write(f"No {constants.TRADES_FILE} found.")
        if st.button("Generate dummy trades"):
            generate_trades.generate_dummy_trades()
            load_trades()
    else:
        st.write(f"{constants.TRADES_FILE} found. Proceeding to load")
        load_trades()
# Data Loader
with prices_tab:
    if st.button("Trigger web scraper"):
        dbm.scrape_prices()
    prices = dbm.get_prices()
    st.write("Prices from db:")
    st.dataframe(prices)
    dbm.graph_prices()
# dbm.insert_prices(trades)
# dbm.read_csv(constants)
# prices = dbm.get_prices()
# trades = dbm.get_trades()
# dbm.get_prices

# Portfolio Manager
# generate_trades.generate_dummy_trades()
