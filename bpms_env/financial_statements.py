# financial_statements.py

from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(filename='financial_data.log', level=logging.ERROR)

# Define the base (SQLAlchemy 2.0)
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

    def to_dict(self):
        return {
            "id": self.id,  # id 추가
            "company_name": self.company_name,
            "report_type": self.report_type,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "total_revenue": self.total_revenue,
            "operating_income": self.operating_income,
            "net_income": self.net_income,
            "total_assets": self.total_assets,
            "total_liabilities": self.total_liabilities,
            "cash_from_operations": self.cash_from_operations,
            "cash_from_investing": self.cash_from_investing,
            "cash_from_financing": self.cash_from_financing
        }

# Database connection
DATABASE_URL = 'postgresql://rainstar:12341234@localhost:5432/hydroponics_db'
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the financial_statements table if it doesn't exist
Base.metadata.create_all(engine)

# Example financial data list
financial_data_list = [
    {
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
    },
    # ... 다른 데이터들도 리스트에 추가
]

# Convert period_start and period_end to datetime.date
def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()

for financial_data in financial_data_list:
    financial_data['period_start'] = parse_date(financial_data['period_start'])
    financial_data['period_end'] = parse_date(financial_data['period_end'])

# Save data to the database with duplication check
def save_to_database(data):
    session = SessionLocal()
    try:
        # 중복 여부 확인
        existing_statement = session.query(FinancialStatement).filter_by(
            company_name=data['company_name'],
            report_type=data['report_type'],
            period_start=data['period_start'],
            period_end=data['period_end']
        ).first()

        if existing_statement:
            print(f"이미 존재하는 데이터: {data['company_name']} - {data['report_type']} - {data['period_start']} ~ {data['period_end']}")
        else:
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
            session.commit()
            print("Financial data saved successfully.")
    except Exception as e:
        logging.error(f"Error occurred while saving data: {e}")
        session.rollback()
    finally:
        session.close()

# Iterate over financial_data_list and save each record
for data in financial_data_list:
    save_to_database(data)
