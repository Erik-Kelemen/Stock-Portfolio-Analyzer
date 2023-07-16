# Stock Portfolio Analyzer

The Stock Portfolio Analyzer is an easy to use open-source Python application that allows users to upload CSVs of stock trades and view their portfolio’s P&L, Net Asset Value, volatility, alpha, beta, and Sharpe ratio over time.
The application reads the user's portfolio into a SQLite3 database and scrapes the web for real-world historical stock prices of the involved tickers. It also downloads the treasury bill rates necessary for computing the risk-free rate for the Sharpe ratio. 
The portfolio calculates Net Asset Value across time efficiently using through the use of matrix multiplication and NumPy broadcasting while accounting for currency conversion (USD and CAD are currently supported). 

The analyzer also empowers users with advanced risk management tools, including Value at Risk (VaR) and efficient frontier analysis.

All this data is presented on an intuitive, easy to use Streamlit dashboard for users to view an in-depth analysis of their portfolio.

## Architecture
![alt text](https://github.com/Erik-Kelemen/Stock-Portfolio-Analyzer/blob/main/imgs/StockPortfolioAnalyzer.drawio.png)

## Components
The framework consists of three primary components, plus an auxiliary Utils folder for generating dummy trade portfolios:

### 1. DataSource
#### dummy_trades.py
Randomly generates a valid dummy trading portfolio with the following stocks between 2022-01-01 and 2022-12-31, ignoring all weekends and market holidays -- 'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', "RY.TO", "SHOP.TO", "BNS.TO", "TD.TO", "ENB.TO". A "valid" portfolio is one that never tries to sell more shares of a particular stock than it holds. The output file will be written to data/trades.csv. Be careful if you do not want this overwritten!

You can skip this step if you can supplement your own prices.csv, as long as it follows the specified format. Please refer to data/prices.csv for formatting examples. 

### 2. DataManager:
#### data_loader.py
Populates the local SQLite3 database of prices with the columns date, time, ticker, price, and currency, by calling the web scraper with the list of tickers to download data for and the appropriate date range.

#### web_scraper.py
Web scraper for the S&P 500 and Toronto exchange (TSX) using yfinance. Accepts a list of tickers to scrape for and a date range to query between, and uploads the results to the SQLite3 database and returns the results as a dataframe.
You can replace this with your own web scraper to procure the required data.

### 3. PortfolioAnalyzer:
#### controller.py
Manages the communication layer between the prices.csv & trades.csv files with the trading_strategy class. Parses and loads the prices.csv file into a pandas dataframe to pass into the TradingStrategy. Filters for a specified lookback period (default 10 days) of the pool of stocks and delivers it to the system. 

#### portfolio_calc.py
Computes portfolio P&L, Net Asset Value, volatility, alpha, beta, and Sharpe ratio over time. It leverages matrix multiplication and numpy broadcasting to optimize calculations, taking into account currency conversions.

#### risk_analyzer.py
Computes portfolio Value at Risk (VaR) and efficient frontier analysis (EFA) over time. 

#### analyzer.py
Performs 

### 4. Dashboard: 
#### dashboard.py
A lightweight Streamlit dashboard for data viz and insights.


## How to Use
Follow these steps to use the Trading Algorithm Backtester:

1. Use your favorite package manager (I use pip) to install the popular yfinance, Pandas, NumPy, Requests, BeautifulSoup, and Streamlit libraries. 
2. Upload your trading portfolio as a CSV file with the columns date, ticker, quantity, to the data/ directory. If you do not have one, you can randomly generate one with the Utils/generate_trades.py script.
3. Run DataAccessor/data_loader.py to spin up a local SQLite3 database to load the prices and trades into. This will automatically perform the web scraping for you.
4. Run controller.py to compute the quantitative metrics.
5. Run the streamlit dashboard with ```run streamlit interface.py``` in the interface directory.
6. Feel free to customize and integrate the Stock Portfolio Analyzer into your own projects.

## Future Work
This project can be extended to improve robustness, flexibility, accuracy, reliability, and usefulness. Here are just some of my ideas:
1. Intraday Analysis: This analyzer provides insight on a per-day level of granularity. In real world scenarios, this constraint is very restrictive -- consider adding scraping functionality on a per-30 minute time basis (or more frequent!) to also conduct the same analysis on (yfinance supports this).
2. Transaction Costs: This analyzer overlooks transaction costs such as brokerage fees, commissions, exchange fees, and bid-ask spreads. These costs can eat into profits and impact the overall performance of a trading strategy or portfolio. Consider introducing a configurable "transaction fee" constant which deducts from profits and assets linearly with number of trades.
3. Order Types and Timing: This analyzer only accepts portfolios of market orders. However, in practice, traders use various types of orders, such as limit orders, stop-loss orders, trailing stops, or iceberg orders. The timing of order placement and cancellation, as well as the order routing mechanism, can also influence trading outcomes.
4. Support for more diverse portfolios: To improve the robustness and accuracy of the backtester should be diversifying the stock portfolio and adding more foreign currencies from other exchanges. This may include adding additional web scrapers and sourcing to the DataManager. It also reduced dependency on the yfinance API.


## Closing Thoughts
Please note that this README provides a brief overview of the system. For more detailed instructions and examples, refer to the comments within the source code or reach out to me at kelemen.erik@gmail.com.

Enjoy analyzing and evaluating stock portfolio performance using the Stock Portfolio Analyzer!
