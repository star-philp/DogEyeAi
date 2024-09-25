from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the base (Update this for SQLAlchemy 2.0)
Base = declarative_base()

# Define your financial statement model
class FinancialStatement(Base):
    __tablename__ = 'financial_statements'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255))
    report_type = Column(String(255))  # income statement, balance sheet, etc.
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

# Step 2: Create a database connection
DATABASE_URL = 'postgresql://rainstar:12341234@localhost:5432/hydroponics_db'
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Step 3: Create the financial_statements table if it doesn't exist
Base.metadata.create_all(engine)

# Step 4: Example financial data
financial_data = {
    'company_name': 'Company A',
    'report_type': 'Income Statement',
    'period_start': '2020-01-01',
    'period_end': '2020-12-31',
    'total_revenue': 5000000,
    'operating_income': 2000000,
    'net_income': 1500000,
    'total_assets': 10000000,
    'total_liabilities': 4000000,
    'cash_from_operations': 2500000,
    'cash_from_investing': -500000,
    'cash_from_financing': 1000000
}

# Step 5: Save data to the database
def save_to_database(data):
    new_statement = FinancialStatement(
        company_name=data['company_name'],
        report_type=data['report_type'],
        period_start=data['period_start'],
        period_end=data['period_end'],
        total_revenue=data['total_revenue'],
        operating_income=data['operating_income'],
        net_income=data['net_income'],
        total_assets=data['total_assets'],
        total_liabilities=data['total_liabilities'],
        cash_from_operations=data['cash_from_operations'],
        cash_from_investing=data['cash_from_investing'],
        cash_from_financing=data['cash_from_financing']
    )
    
    session.add(new_statement)
    session.commit()  # Save changes to the database
    session.close()

# Call the function with the example data
save_to_database(financial_data)
