from config.db import get_db_connection
from utils.hash import hash_password_sha3, verify_password_sha3
import mysql.connector

def check_user_login(username: str, password: str) -> tuple[bool, int | None]:
    """
    Memverifikasi login user.
    Mengembalikan (True, user_id) jika berhasil, (False, None) jika gagal.
    """
    conn = get_db_connection()
    if conn is None:
        return False, None

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Ambil user berdasarkan username
        query = "SELECT id, password_hash FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        if user:
            # 1. Hapus logika 'else' dan 'tuple' (user[0])
            #    Karena Anda menggunakan dictionary=True, 'user' PASTI dictionary.
            user_id = int(user['id']) # type: ignore
            stored_hash = str(user['password_hash']) # type: ignore

            # 2. Perbaiki 'return' dengan menambahkan '#'
            if verify_password_sha3(password, stored_hash):
                return True, user_id  # Login berhasil
            
        # Baris ini akan berjalan jika password salah ATAU user tidak ditemukan
        return False, None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False, None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def create_user(username: str, password: str) -> bool:
    """Membuat user baru (untuk registrasi)."""
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        hashed_password = hash_password_sha3(password)
        cursor = conn.cursor(dictionary=True)
        
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        # 23000 (Integrity constraint violation) atau 1062 (Duplicate entry)
        if err.errno == 1062: 
            print("Error: Username already exists.")
        else:
            print(f"Error: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()