from sqlalchemy import create_engine

DATABASE_URL = "postgresql://rainstar:12341234@localhost:5432/hydroponics_db"
engine = create_engine(DATABASE_URL)

try:
    # Try to connect to the database
    connection = engine.connect()
    print("Database connected successfully")
    connection.close()
except Exception as e:
    print(f"Error connecting to the database: {e}")
