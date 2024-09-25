from sqlalchemy import Column, Integer, String, Numeric, Date
from database import Base

class FinancialStatement(Base):
    __tablename__ = 'financial_statements'

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    report_type = Column(String)
    period_start = Column(Date)
    period_end = Column(Date)
    total_revenue = Column(Numeric)
    operating_income = Column(Numeric)
    net_income = Column(Numeric)
    total_assets = Column(Numeric)
    total_liabilities = Column(Numeric)
    cash_from_operations = Column(Numeric)
    cash_from_investing = Column(Numeric)
    cash_from_financing = Column(Numeric)

class StockPrice(Base):
    __tablename__ = 'stock_prices'

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    date = Column(Date)
    open_price = Column(Numeric)
    close_price = Column(Numeric)

class MacroeconomicData(Base):
    __tablename__ = 'macroeconomic_data'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    indicator = Column(String)
    value = Column(Numeric)

class CorporateNews(Base):
    __tablename__ = 'corporate_news'

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    event_type = Column(String)
    event_date = Column(Date)
    title = Column(String)
    summary = Column(String)
