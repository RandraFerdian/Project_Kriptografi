import mysql.connector
import streamlit as st

DB_CONFIG = {
    'host': "127.0.0.1",
    'user': "root",
    'password': "", # Isi password Anda jika ada
    'database': "kriptografi"
}

def get_db_connection():
    """Membuat dan mengembalikan koneksi database baru."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error connecting to database: {err}")
        return None