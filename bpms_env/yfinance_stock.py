import yfinance as yf

# Fetch stock data for Apple (AAPL) from 2016-01-01 to 2021-12-31
ticker = yf.Ticker("AAPL")
stock_data = ticker.history(start="2016-01-01", end="2021-12-31")

# Print the stock data
print(stock_data)