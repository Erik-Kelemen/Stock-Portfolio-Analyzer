import csv
import datetime
import yfinance as yf

# Define the date range
start_date = datetime.datetime(2023, 6, 1)
end_date = datetime.datetime(2023, 7, 15)
time_intervals = ['09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30',
                  '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00']

# Generate the CSV file
with open('../data/prices.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['date', 'time', 'ticker', 'bid', 'ask', 'currency'])

    current_date = start_date
    while current_date <= end_date:
        for interval in time_intervals:
            dt = datetime.datetime.combine(current_date.date(), datetime.datetime.strptime(interval, '%H:%M').time())
            data = yf.download('^GSPC', start=dt, end=dt+datetime.timedelta(minutes=29), interval='30m')
            # data = yf.download("^GSPC", stsart=dt, end)
            if not data.empty:
                ticker = '^GSPC'
                bid = round(data['Close'][0], 2)
                ask = round(data['Close'][0] + 1.0, 2)  # Adjust the ask price as desired
                currency = 'USD'

                writer.writerow([current_date.strftime('%Y-%m-%d'), interval, ticker, bid, ask, currency])

        current_date += datetime.timedelta(days=1)