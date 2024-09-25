# from sqlalchemy import create_engine, inspect

# DATABASE_URL = "postgresql://rainstar:12341234@localhost:5432/hydroponics_db"
# engine = create_engine(DATABASE_URL)

# # Inspect the database and get the table names
# inspector = inspect(engine)
# print(inspector.get_table_names())

# # Check if 'stock_prices' table exists and list its columns
# columns = inspector.get_columns('stock_prices')
# for column in columns:
#     print(f"Column: {column['name']} - Type: {column['type']}")

import yfinance as yf
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database connection URL
DATABASE_URL = "postgresql://rainstar:12341234@localhost:5432/hydroponics_db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the Base for the ORM models
Base = declarative_base()

# Define the stock prices table model
class StockPrice(Base):
    __tablename__ = 'stock_prices'
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    date = Column(Date)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(BigInteger)
    dividends = Column(Float)
    stock_splits = Column(Float)

# Create the stock_prices table in the database
Base.metadata.create_all(bind=engine)

# Function to save stock data to the database
# Function to save stock data to the database
def save_stock_data(ticker_symbol):
    # Fetch stock data using yfinance
    ticker = yf.Ticker(ticker_symbol)
    stock_data = ticker.history(start="2016-01-01", end="2021-12-31")

    # Create a new database session
    db = SessionLocal()

    # Iterate over each row in the stock_data DataFrame
    for index, row in stock_data.iterrows():
        stock_price = StockPrice(
            company_name=ticker_symbol,
            date=index.date(),
            open_price=float(row['Open']),
            high_price=float(row['High']),
            low_price=float(row['Low']),
            close_price=float(row['Close']),
            volume=int(row['Volume']),
            dividends=float(row['Dividends']) if 'Dividends' in row else 0.0,  # Set default to 0.0 if missing
            stock_splits=float(row['Stock Splits']) if 'Stock Splits' in row else 0.0  # Set default to 0.0 if missing
        )

        # Add the stock_price record to the session
        db.add(stock_price)

    # Commit the session to save the data to the database
    db.commit()
    db.close()

save_stock_data("AAPL")

