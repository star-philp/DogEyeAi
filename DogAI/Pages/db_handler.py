import psycopg2
from psycopg2 import sql
import pandas as pd
import streamlit as st
import os

def is_db_configured():
    """DB 연결 정보가 설정되어 있는지 확인"""
    if "database" in st.secrets:
        return True
    return bool(os.environ.get('DB_HOST'))

def connect_to_db():
    try:
        if not is_db_configured():
            return None

        # Use st.secrets if available (for Streamlit Cloud), otherwise use environment variables
        if "database" in st.secrets:
            secrets = st.secrets["database"]
            host = secrets.get("DB_HOST", "db.xrlwfdazmevlqgozkecc.supabase.co")
            port = secrets.get("DB_PORT", "5432")
            dbname = secrets.get("DB_NAME", "postgres")
            user = secrets.get("DB_USER", "postgres")
            password = secrets.get("DB_PASSWORD", "")
        else:
            host = os.environ.get('DB_HOST', 'host.docker.internal')
            port = os.environ.get('DB_PORT', '5433')
            dbname = os.environ.get('DB_NAME', 'dog_health')
            user = os.environ.get('DB_USER', 'rainstar')
            password = os.environ.get('DB_PASSWORD', '007008')
        
        conn = psycopg2.connect(
            dbname=dbname, 
            user=user, 
            password=password, 
            host=host,
            port=port
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
