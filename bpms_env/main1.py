from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import FinancialStatement
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware to allow cross-origin requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development (update for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(level=logging.DEBUG)  # Set to debug level for detailed logs
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
    period_start: str  # Convert to string format
    period_end: str  # Convert to string format
    total_revenue: float
    operating_income: float
    net_income: float
    total_assets: float
    total_liabilities: float
    cash_from_operations: float
    cash_from_investing: float
    cash_from_financing: float

    class Config:
        from_attributes = True  # Updated for Pydantic v2

# Define a response model
class FinancialDataResponse(BaseModel):
    data: List[FinancialStatementBase]
    total: int

# No changes needed for Config here, but if you had orm_mode, update it
# class Config:
#     from_attributes = True  # Updated for Pydantic v2

# Get financial data with filters and pagination
@app.get("/financial_data/", response_model=FinancialDataResponse)
def get_financial_data(
    company_name: str = '',
    start_date: str = '',
    end_date: str = '',
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(FinancialStatement)
        logger.info(f"Received API request with filters: company_name={company_name}, start_date={start_date}, end_date={end_date}")

        # Filter by company name if provided
        if company_name:
            query = query.filter(FinancialStatement.company_name.ilike(f'%{company_name}%'))

        # Filter by date range if both start_date and end_date are provided
        if start_date and end_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                query = query.filter(
                    FinancialStatement.period_start >= start_date_obj,
                    FinancialStatement.period_end <= end_date_obj
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

        total_records = query.count()
        data = query.offset((page - 1) * limit).limit(limit).all()

        if not data:
            logger.warning("No financial data found for the given filters.")
            return {"data": [], "total": 0}

        # Convert date objects to strings
        for item in data:
            item.period_start = item.period_start.strftime('%Y-%m-%d')
            item.period_end = item.period_end.strftime('%Y-%m-%d')

        logger.info(f"Returning {len(data)} financial records.")
        return {"data": data, "total": total_records}

    except Exception as e:
        logger.error(f"Error fetching financial data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Start FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
