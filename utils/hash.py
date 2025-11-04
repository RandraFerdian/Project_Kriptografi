import hashlib

def hash_password_sha3(password: str) -> str:
    """Meng-hash password menggunakan SHA3-512."""
    # Pastikan password di-encode ke bytes sebelum di-hash
    password_bytes = password.encode('utf-8')
    
    # Menggunakan SHA3-512 (menghasilkan hash 128 karakter hex)
    # Kolom Anda varchar(255), jadi ini sangat cukup.
    hash_obj = hashlib.sha3_512(password_bytes)
    
    # Mengembalikan representasi heksadesimal dari hash
    return hash_obj.hexdigest()

def verify_password_sha3(plain_password: str, hashed_password: str) -> bool:
    """Memverifikasi apakah plain password cocok dengan hash."""
    # Hash password yang diinput, lalu bandingkan
    return hash_password_sha3(plain_password) == hashed_password