import pandas as pd
import numpy as np
import sqlite3

import config
import data_access
import port_calcs


if __name__ == "__main__":
    prices = data_access.load_prices();
    trades = data_access.load_trades();
    print(prices.head())
    print(trades.head())
    
    # results = dict()
    #
    # results['corr1'] = port_calcs.port_correl(1001, 1005, "2013-01-01", "2013-02-15", trades, prices)
    # results['corr2'] = port_calcs.port_correl(1001, 1005, "2013-01-20", "2013-03-01", trades, prices)
    # results['corr3'] = port_calcs.port_correl(1001, 1005, "2013-01-01", "2013-02-28", trades, prices)
    #
    # results['avg1'] = port_calcs.avg_ret_30min(1001, "2013-01-01", "2013-02-28", trades, prices)
    # results['avg2'] = port_calcs.avg_ret_30min(1005, "2013-01-01", "2013-02-28", trades, prices)
    #
    # print(results)

