import mysql.connector
from config.db import get_db_connection

def add_history_entry(user_id: int, data_type: str, original_data: str, encrypted_data: str) -> bool:
    """
    Menambahkan entri baru ke tabel history.
    """
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        INSERT INTO history (user_id, data_type, original_data, encrypted_data) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, data_type, original_data, encrypted_data))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error adding history: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_history_by_user(user_id: int) -> list:
    """
    Mengambil semua riwayat untuk user_id tertentu, diurutkan dari yang terbaru.
    """
    conn = get_db_connection()
    if conn is None:
        return []
    
    try:
        # Set cursor to return results as dictionary
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM history WHERE user_id = %s ORDER BY created_at DESC"
        cursor.execute(query, (user_id,))
        history_data = cursor.fetchall()
        return list(history_data) if history_data is not None else []
    except mysql.connector.Error as err:
        print(f"Error fetching history: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def delete_history_entry(history_id: int, user_id: int) -> bool:
    """
    Menghapus satu entri history, memastikan user_id cocok (keamanan).
    """
    conn = get_db_connection()
    if conn is None: 
        return False
    try:
        cursor = conn.cursor()
        # Menambahkan user_id di klausa WHERE mencegah user menghapus histori user lain
        query = "DELETE FROM history WHERE id = %s AND user_id = %s"
        cursor.execute(query, (history_id, user_id))
        conn.commit()
        # rowcount > 0 berarti penghapusan berhasil
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"Error deleting history: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()