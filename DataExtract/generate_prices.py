import csv
import datetime
import yfinance as yf
import random
import pandas as pd
import os

def load_SNP500_tickers():
    filepath = 'S&P_500_tickers.txt'

    if os.path.exists(filepath):
        print(f"Tickers file found, loading from {filepath}")
        with open(filepath, 'r') as file:
            all_tickers = [line.strip() for line in file]
    else:
        print(f"No tickers file found, web scraping and writing to {filepath}.")
        URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tickers = pd.read_html(URL)[0]
        all_tickers = tickers.Symbol.to_list()
        with open(filepath, 'w') as file:
            file.writelines('\n'.join(all_tickers))
    print(f"Tickers loaded: {all_tickers}")
    return all_tickers

def load_prices(target_file, selected_tickers, start_date, end_date, time_intervals):
    with open(target_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'time', 'ticker', 'bid', 'ask', 'currency'])

        current_date = start_date
        while current_date <= end_date:
            for interval in time_intervals:
                for ticker in selected_tickers:
                    dt = datetime.datetime.combine(current_date.date(), datetime.datetime.strptime(interval, '%H:%M').time())
                    try:
                        data = yf.download(ticker, start=dt, end=dt + datetime.timedelta(minutes=30), interval='1d')
                    except Exception as e:
                        print(f"No data available for {ticker} on {current_date.strftime('%Y-%m-%d')} - Skipping.")
                        continue

                    if not data.empty:
                        bid = round(data['Close'][0], 2)
                        ask = round(data['Close'][0] + 1.0, 2)  
                        currency = 'USD'
                        writer.writerow([current_date.strftime('%Y-%m-%d'), interval, ticker, bid, ask, currency])

            current_date += datetime.timedelta(days=1)

def generate_prices(target_file = '../data/gen_prices.csv'):
    all_tickers = load_SNP500_tickers()
    num_tickers = 30
    selected_tickers = random.sample(all_tickers, num_tickers)

    # Establish date range 
    start_date = datetime.datetime(2023, 6, 1)
    end_date = datetime.datetime(2023, 6, 2)
    time_intervals = ['09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30',
                    '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00']

    load_prices(target_file, selected_tickers, start_date, end_date, time_intervals)

if __name__ == "__main__":
    generate_prices()
