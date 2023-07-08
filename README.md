# Stock Portfolio Valuation System

The Stock Portfolio Valuation System (SPVS) is an easy-to-integrate open-source Python framework designed for quantitative analysis of stock portfolio performance for stocks on the S&P 500. 

## Components
The framework consists of the following five components:

### 1. DataExtract: 
This component generates the prices.csv and trades.csv files. You can replace it with your own web scraper or data extraction tools to procure the required prices and trades data. Please refer to the data/prices.csv and data/trades.csv files for formatting examples. It is currently set up to scrape the web for historical S&P 500 stock prices using the popular open-source yfinance library. Portfolios are generated pseudo-randomly using standard Python Random-Number-Generation (RNG) and are represented in trades.csv.

### 2. DataLoader: 
The DataLoader component parses the prices.csv and trades.csv files and stores them in the SQLite3 database located in data/sql_data.db (defined in setup.py). It also handles the retrieval of data from the database using data_access.py.

### 3. CalculationEngine: 
The CalculationEngine is responsible for calculating returns. It leverages matrix multiplication and numpy broadcasting to optimize the calculations of portfolio positions and Net Asset Values (NAVs) over time, taking into account currency conversions.

### 4. QuantEngine: 
The QuantEngine computes correlation coefficients between portfolios, as well as alphas and betas of different hedging strategies.

### 5. Regression: 
The Regression component performs ridge and lasso regressions.

## How to Use
Follow these steps to use the Stock Portfolio Valuation System:

1. Install the popular open-source yfinance library if you do not yet have it if you plan to use DataExtract. To do this, run:
   ```
   pip install yfinance
   ```
2. Download a S&P 500 stock prices and a randomly generated portfolio. If you have your own prices.csv and trades.csv files, you can skip this step and add them to the /data/ directory. 
3. Run DataLoader/setup.py to start up the necessary database and dependencies.
4. Trigger main.py with the desired function to perform the analysis.
5. Feel free to customize and integrate the Stock Portfolio Valuation System into your own projects.

Please note that this README provides a brief overview of the system. For more detailed instructions and examples, refer to the comments within the source code or reach out to me at kelemen.erik@gmail.com.

Enjoy analyzing and evaluating stock portfolio performance using the Stock Portfolio Valuation System!
