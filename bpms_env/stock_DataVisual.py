import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

# Connect to your database
DATABASE_URL = "postgresql://rainstar:12341234@localhost:5432/hydroponics_db"
engine = create_engine(DATABASE_URL)

# Query the data
query = """
SELECT date, close_price FROM stock_prices WHERE date BETWEEN '2016-01-01' AND '2016-12-31' ORDER BY date;
"""
df = pd.read_sql(query, engine)

# Plot the closing prices
plt.plot(df['date'], df['close_price'], label='Closing Price')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('AAPL Closing Prices in 2016')
plt.legend()
plt.show()
