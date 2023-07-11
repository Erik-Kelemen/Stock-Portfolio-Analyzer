# Trading Algorithm Backtester

The Trading Algorithm Backtester is an easy to use open-source Python framework for backtesting algorithmic trading strategies on historical S&P 500 and TSX stock prices, enabling users to implement technical trading algorithms and view portfolio performance in P&L. The backtester takes snapshots of stock prices at fixed timestamps from 9:30 to 16:00 by intervals of 30 minutes for a list of companies from the S&P 500 and TSX exchange and feeds them to the CalculationEngine for computing the positions and Net Asset Values (NAVs) of the portfolio.

## Components
The framework consists of the following four components:

### 1. DataLoader:
#### generate_prices.py
Creates a CSV of prices with the columns date, time, ticker, price, and currency. Web scrapes for S&P 500 and Toronto exchange (TSX) companies and takes a random sample of 30 USD and 5 CAD stocks for the trading data. You can customize this to fit the time frame and number of stocks you want. The data extractor then downloads prices for the list of stocks for every 30 minute interval during the trading day (09:30 to 16:00) for the range of dates provided.

You can replace this with your own web scraper to procure the required data, or you can supplement your own prices.csv, as long as it follows the specified format. Please refer to the data/prices.csv for more formatting examples. 

### 2. TradingEngine:
#### controller.py
Manages the communication layer between the prices.csv & trades.csv files with the trading_strategy class. Parses and loads the prices.csv file into a pandas dataframe to pass into the TradingStrategy. Filters for a specified lookback period (default 10 days) of the pool of stocks and delivers it to the system. 

#### trading_engine.py
This is the primary module for you to implement. The default trading engine generates trades randomly from the available options so long as they do not exceed the value of the current cash.

### 3. PortfolioManager: 
#### position_calculator.py
Responsible for calculating all portfolio positions and Net Asset Values (NAVs) across time. It leverages matrix multiplication and numpy broadcasting to optimize calculations, taking into account currency conversions.

#### quantitative_calculator.py
Computes correlation coefficients between portfolios, as well as alphas, betas, and sharpe ratios of different hedging strategies.

### 4. TODO: Regression: 
The Regression component performs ridge and lasso regressions.

## How to Use
Follow these steps to use the Trading Algorithm Backtester:

1. To use DataExtract, use your favorate package manager (I use pip) to install the popular open-source yfinance, Pandas, NumPy, Requests, and BeautifulSoup libraries. 
2. Download S&P 500 stock prices and a randomly generated portfolio. If you have your own prices.csv and trades.csv files, you can skip this step and add them to the /data/ directory. 
3. Run DataLoader/setup.py to start up the necessary database and dependencies.
4. Trigger main.py with the desired function to perform the analysis.
5. Feel free to customize and integrate the Stock Portfolio Valuation System into your own projects.

Please note that this README provides a brief overview of the system. For more detailed instructions and examples, refer to the comments within the source code or reach out to me at kelemen.erik@gmail.com.

Enjoy analyzing and evaluating stock portfolio performance using the Trading Algorithm Backtester!
