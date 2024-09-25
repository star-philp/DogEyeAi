from sqlalchemy.orm import Session
from database import SessionLocal
from models import MacroeconomicData

def populate_data():
    db = SessionLocal()
    data_entries = [
        MacroeconomicData(date='2021-01-01', indicator='GDP Growth', value=3.5),
        MacroeconomicData(date='2021-01-01', indicator='Inflation Rate', value=1.2),
        MacroeconomicData(date='2021-01-01', indicator='Interest Rate', value=0.5),
        MacroeconomicData(date='2021-04-01', indicator='GDP Growth', value=4.0),
        MacroeconomicData(date='2021-04-01', indicator='Inflation Rate', value=1.5),
        MacroeconomicData(date='2021-04-01', indicator='Interest Rate', value=0.75),
        # Add more data as necessary
    ]
    db.add_all(data_entries)
    db.commit()
    db.close()

if __name__ == "__main__":
    populate_data()
