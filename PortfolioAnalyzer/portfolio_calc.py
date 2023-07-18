# import pandas as pd
# import numpy as np
from datetime import datetime

import pandas as pd
import numpy as np

from Accessor import data_loader
from PortfolioAnalyzer import portfolio_calc

class PortfolioCalculator:
    def PortfolioCalculator(prices, trades):
        pass

    #mapped {date,time} --> conversion rate
    def CAD_to_USD(date, time, currency, price, date_time_to_rate):
        """
        Utility function for converting USD to CAD for a specific date and time.
        """
        return price if currency == 'USD' else price * (1 / date_time_to_rate[(date, time)][2])
    #     Assumptions:
    # 1. Trades represent changes to the positions and are transferred into the portfolio before the market 
    #  open. 
    # 2. Portfolio NAV is computed as the sum value of CASH + long positions – short positions using the mid 
    #  price at that time.
    # 3. Portfolio NAV is assumed to be $0 prior to the first trade date.
    #I have treated CASH_USD as cash transfers into the portfolio.
    # Return = (NAV_F - NAV_B) / NAV_B
    #Time * Date * Stocks  PRICES (for all stocks)
    #STOCK * DATE TRADES (for all stocks)k
    def nav(port_id, start_date, end_date, trades, prices):
        """
        Returns the Net Asset Value (NAV) per day for the date range.
        Should return a Series with 1 value for each time bucket.
        """
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        prices['mid'] = prices[['bid', 'ask']].mean(axis=1)
        date_time_to_rate = prices[(prices['ticker'] == 'USD/CAD')].set_index(['date','time'])['mid']

        trades = trades[(trades['port_id'] == port_id)].copy()
        prices = prices[(prices['ticker'] != 'USD/CAD')].copy()
        prices['mid_USD'] = prices.apply(lambda row: 
                                        CAD_to_USD(row['date'], row['time'], row['currency'], row['mid'], date_time_to_rate), 
                                        axis=1)
        
        times, dates, tickers = prices['time'].unique(), prices['date'].unique(), prices['ticker'].unique()
        m, n, p = len(times), len(dates), len(tickers)
        prices = prices[['time','date', 'ticker', 'mid_USD']]
        
        df = prices.groupby(['time', 'date', 'ticker'])['mid_USD'].mean().reset_index()
        A = df['mid_USD'].to_numpy()
        A = A.reshape((m, n, p))
        
        #p*n
        trades = trades[['date','ticker','qty']]
        
        #i think we need to create a pandas dataframe
        #with same # of rows and columns
        #B is going to be the holdings...
        #if i can order by ticker, i can populate the rows by doing all the ticker dates...
        #if i order by date, it would be more like columns, but i could go column-major order...
        #or i could do row-major order and then transpose it
        #i like that idea best
        #make an n*p instead and compile list and do it like a prefix sum with dictionary representing row state
        df2 = pd.DataFrame(np.zeros((p,n)), index=tickers)
        trades = trades.groupby(['date', 'ticker']).mean().reset_index()
        print(trades)
        # holdings = {date: }
        # for date in dates:
        #     subset = trades[(trades['date'] == date)]
        #     for row in subset:

        # for ind, rows in trades.iterrows():
        #     df2['row'] = 1;
        # print(df2.head())
        B = np.zeros((p,n))
        
        print(B)
        # print(trades)
        # pivot_table = pd.pivot_table(trades, values='qty', index = df['ticker'], columns=df['date'], fill_value=0)
        # B = pivot_table.to_numpy()
        # print(B)
        # df = filt_prices.groupby('time').agg({'date'})
        # C = np.einsum('mnr,rn->mn', A, B)
        # C = C.flatten('F')
        
        # filt_prices['NAV'] = C
        # filt_prices['lag_NAV'] = filt_prices['NAV'].shift(1)
        # filt_prices['return'] = (filt_prices['NAV'] - filt_prices['lag_NAV']) / filt_prices['lag_NAV']
        
        # filt_prices = filt_prices(filt_prices['date'].between(start_date, end_date))
        #filt_prices = filt_prices[(start_date <= filt_prices['date] <= end_date)]
        # avg_ret_30m = filt_prices['return'].groupby('time')
        # ans = avg_ret_30m['return'].mean()
        # print(ans)
        # return ans
        return 0

    def profits_and_losses():
        pass
    def alphas():
        pass
    def betas():
        pass
    def sharpe_ratios():
        pass
    


if __name__ == "__main__":
    prices = data_access.load_prices();
    trades = data_access.load_trades();

    results = dict()
