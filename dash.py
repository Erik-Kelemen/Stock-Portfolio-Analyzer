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
st.write("Welcome to the Stock Portfolio Analyzer. Made by Erik Kelemen.")

# Dummy Trades
if st.button("Generate dummy trades"):
    generate_trades.generate_dummy_trades()

# Data Loader
dbm = data_loader.DBManager()
trades = dbm.get_trades()
st.write("Trades imported:")
st.dataframe(trades)

prices = dbm.get_prices()
st.write("Prices in db:")
st.dataframe(prices)
# dbm.insert_prices(trades)
# dbm.read_csv(constants)
# prices = dbm.get_prices()
# trades = dbm.get_trades()
# dbm.get_prices

# Portfolio Manager
# generate_trades.generate_dummy_trades()
