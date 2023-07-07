Stock Portfolio Valuation System

The Stock Portfolio Valuation System (SPVS) is an easy-to-integrate open-source Python framework designed for quantitative analysis of stock portfolio performance.

Components
The framework consists of the following five components:

DataExtract: This component generates the prices.csv and trades.csv files. You can replace it with your own web scraper or data extraction tool to generate the required price and trade data. Please refer to the data/prices.csv and data/trades.csv files for formatting examples. The component uses standard Python random number generation (RNG) to calculate stock trades, ticker symbols, and in/out dates in a flexible and easy-to-parameterize manner.

DataLoader: The DataLoader component parses the prices.csv and trades.csv files and stores them in the SQLite3 database located in data/sql_data.db (defined in setup.py). It also handles the retrieval of data from the database using data_access.py.

CalculationEngine: The CalculationEngine is responsible for calculating returns. It leverages matrix multiplication and numpy broadcasting to optimize the calculations of portfolio positions and Net Asset Values (NAVs) over time, taking into account currency conversions.

QuantEngine: The QuantEngine computes correlation coefficients between portfolios, as well as alphas and betas of different hedging strategies.

Regression: The Regression component performs ridge and lasso regressions.

How to Use
Follow these steps to use the Stock Portfolio Valuation System:

Add your own prices.csv and trades.csv files to the /data/ directory.
Run setup.py to set up the necessary database and dependencies.
Trigger main.py with the desired function to perform the analysis.
Feel free to customize and integrate the Stock Portfolio Valuation System into your own projects.

Please note that this README provides a brief overview of the system. For more detailed instructions and examples, refer to the documentation or comments within the source code.

Enjoy analyzing and evaluating stock portfolio performance using the Stock Portfolio Valuation System!