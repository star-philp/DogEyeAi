import fetch_data as yf

# Fetching financial data for Apple (AAPL) as an example
ticker = yf.Ticker("AAPL")

# Downloading the financial statements
income_statement = ticker.financials
balance_sheet = ticker.balance_sheet
cash_flow = ticker.cashflow

# Show the last 5 years of financial dataprint("Income Statement (Last 5 Years):\n", income_statement)
print("Balance Sheet (Last 5 Years):\n", balance_sheet)
print("Cash Flow (Last 5 Years):\n", cash_flow)