"""
Contains constant configuration variables
"""
# import streamlit as st
import os
HOME_DIR = os.getcwd()
DB_FILE = f"{HOME_DIR}/data/sql_data.db"
PRICES_FILE = f"{HOME_DIR}/data/prices.csv"
TRADES_FILE = f"{HOME_DIR}/data/trades.csv"
