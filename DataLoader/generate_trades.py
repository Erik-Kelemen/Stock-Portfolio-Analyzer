import csv
import random
from datetime import datetime, timedelta

# Define the date range
start_date = datetime(2023, 6, 1)
end_date = datetime(2023, 7, 8)

# Define the list of tickers
tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB']

# Define the number of portfolios and unique port_ids
num_portfolios = 5
unique_port_ids = ['P1', 'P2', 'P3', 'P4', 'P5']

# Define the output file path
output_file = 'trades.csv'

# Generate trades data
trades_data = []
current_date = start_date
while current_date <= end_date:
    for port_id in unique_port_ids:
        for ticker in tickers:
            qty = random.choice([-1, 1]) * random.randint(1, 10) * 10  # Randomly generate positive/negative multiples of 10
            trades_data.append([port_id, current_date.strftime('%Y-%m-%d'), ticker, qty])
    current_date += timedelta(days=1)

# Write trades data to CSV file
trades_file = '../data/gen_trades.csv'
with open(trades_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['port_id', 'date', 'ticker', 'qty'])
    writer.writerows(trades_data)

print(f"Trades data generated and saved to {output_file}.")

if __name__ == "__main__":
    generate_prices()
