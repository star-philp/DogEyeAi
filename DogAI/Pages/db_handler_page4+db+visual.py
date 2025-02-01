import psycopg2
from psycopg2 import sql
import pandas as pd
import streamlit as st

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="dog_health", 
            user="rainstar", 
            password="12341234", 
            host="localhost"
        )
        return conn
    except psycopg2.OperationalError as e:
        st.error(f"Database connection failed: {e}")
        return None

def create_table_if_not_exists(conn):
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id SERIAL PRIMARY KEY,
                class TEXT,
                index_value INTEGER,
                probabilities TEXT,
                analysis_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
    except Exception as e:
        st.error(f"Failed to create table: {e}")

def save_results_to_db(conn, pred_class, pred_idx, probs):
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            sql.SQL('''
                INSERT INTO analysis_results (class, index_value, probabilities)
                VALUES (%s, %s, %s)
            '''),
            [str(pred_class), int(pred_idx), str(probs.tolist())]
        )
        conn.commit()
        cursor.close()
    except Exception as e:
        st.error(f"Failed to save results to the database: {e}")

def load_data():
    conn = connect_to_db()
    if conn is None:
        return None

    try:
        query = "SELECT * FROM analysis_results"
        data = pd.read_sql(query, conn)
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None
    finally:
        if conn:
            conn.close()

def close_db_connection(conn):
    if conn:
        conn.close()
