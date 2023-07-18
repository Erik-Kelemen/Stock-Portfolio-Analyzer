import csv
import random
from datetime import datetime, timedelta
import sys
import constants
import pathlib
import os
import streamlit as st
"""
A script for generating a randomized, valid trades.csv file for use in the analyzer.
A valid trades.csv is one that never tries to sell more shares of a ticker than it holds.
Will not overwrite an existing one if there is already a trades.csv in data/.
"""

def generate_dummy_trades():
    if os.path.exists(constants.TRADES_FILE):
        st.write(f"{constants.TRADES_FILE} found! Not overwriting.")
        return
    st.write(f"No file found at {constants.TRADES_FILE}, proceeding to generate one.")
    # Define the date range
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)

    # Define the list of tickers
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', "RY.TO", "SHOP.TO", "BNS.TO", "TD.TO", "ENB.TO"]
    # Market holidays of 2022
    market_holidays = set([datetime(2022, 1, 17), datetime(2022,2,21), datetime(2022,4,15), 
                            datetime(2022, 5, 30), datetime(2022, 6, 20), datetime(2022, 7, 4), 
                            datetime(2022,9,5), datetime(2022, 11, 24), datetime(2022, 11, 25), 
                            datetime(2022, 12, 26)])
    def is_trading_day(date):
        return date.weekday() < 5 and date not in market_holidays

    def trade_today():
        threshold = 0.25 #10% probability of a trade today
        return random.random() <= threshold

    # Generate trades data
    holdings = {tick: 0 for tick in tickers}
    trades_data = []
    current_date = start_date
    while current_date <= end_date:
        if is_trading_day(current_date):
            for ticker in tickers:
                if trade_today():
                    qty = random.choice([-1, 1]) * random.randint(1, 10) * 10  # Randomly generate positive/negative multiples of 10
                    qty = max(qty, -holdings[ticker])
                    if qty != 0:
                        holdings[ticker] += qty
                        trades_data.append([current_date.strftime('%Y-%m-%d'), ticker, qty])
        current_date += timedelta(days=1)

    # Write trades data to CSV file
    with open(constants.TRADES_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'ticker', 'qty'])
        writer.writerows(trades_data)

    st.write(f"Trades data generated and saved to {constants.TRADES_FILE}.")