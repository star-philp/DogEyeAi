from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import MacroeconomicData

app = FastAPI()

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MacroeconomicDataBase(BaseModel):
    date: str
    indicator: str
    value: float

# Get all macroeconomic data
@app.get("/macroeconomic_data/", response_model=List[MacroeconomicDataBase])
def read_data(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    data = db.query(MacroeconomicData).offset(skip).limit(limit).all()
    return data

# Get macroeconomic data for a specific date range
@app.get("/macroeconomic_data/range/", response_model=List[MacroeconomicDataBase])
def read_data_range(start_date: str, end_date: str, db: Session = Depends(get_db)):
    data = db.query(MacroeconomicData).filter(MacroeconomicData.date.between(start_date, end_date)).all()
    return data
