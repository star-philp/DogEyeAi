# financial_api.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from financial_statements import Base, FinancialStatement
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware

# Database setup
DATABASE_URL = 'postgresql://rainstar:12341234@localhost:5432/hydroponics_db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize FastAPI app
app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:3000",  # React 앱이 실행되는 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# /financial_data/ 엔드포인트 정의
@app.get("/financial_data/")
def get_financial_data(
    company_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(FinancialStatement)

    if company_name:
        query = query.filter(FinancialStatement.company_name == company_name)

    if start_date and end_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(
                FinancialStatement.period_start >= start_date_obj,
                FinancialStatement.period_end <= end_date_obj
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    total = query.count()
    results = query.offset((page - 1) * limit).limit(limit).all()

    data = [item.to_dict() for item in results]

    return {
        "data": data,
        "total": total
    }
