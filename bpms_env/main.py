from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import SessionLocal, engine, Base
from models import FinancialStatement, StockPrice
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import logging

# Define your database URL
DATABASE_URL = "postgresql://rainstar:12341234@localhost:5432/hydroponics_db"

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware to allow cross-origin requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for response validation
class FinancialStatementBase(BaseModel):
    company_name: str
    report_type: str
    period_start: str
    period_end: str
    total_revenue: float
    operating_income: float
    net_income: float
    total_assets: float
    total_liabilities: float
    cash_from_operations: float
    cash_from_investing: float
    cash_from_financing: float

class StockPriceBase(BaseModel):
    company_name: str
    date: str
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    volume: int
    dividends: float
    stock_splits: float

# Get financial data
@app.get("/financial_data/", response_model=List[FinancialStatementBase])
def get_financial_data(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    logger.info("Fetching financial data from the database.")
    return db.query(FinancialStatement).offset(skip).limit(limit).all()

# Get stock data
@app.get("/stock_data/", response_model=List[StockPriceBase])
def get_stock_data(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    logger.info("Fetching stock data from the database.")
    return db.query(StockPrice).offset(skip).limit(limit).all()

# Start FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
