# models.py
from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

# FinancialStatement model
class FinancialStatement(Base):
    __tablename__ = "financial_statements"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255))
    report_type = Column(String(255))
    period_start = Column(Date)
    period_end = Column(Date)
    total_revenue = Column(Float)
    operating_income = Column(Float)
    net_income = Column(Float)
    total_assets = Column(Float)
    total_liabilities = Column(Float)
    cash_from_operations = Column(Float)
    cash_from_investing = Column(Float)
    cash_from_financing = Column(Float)

# StockPrice model
class StockPrice(Base):
    __tablename__ = "stock_prices"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255))
    date = Column(Date)
    open_price = Column(Float)
    close_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    volume = Column(Integer)
    dividends = Column(Float)
    stock_splits = Column(Float)
