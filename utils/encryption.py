import base64
import binascii
import itertools
import io
import numpy as np
from PIL import Image
from Cryptodome.Cipher import Salsa20
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Random import get_random_bytes
from typing import Any


#--------------------------------------------------------
#                   FUNGSI CAESAR CIPHER
#--------------------------------------------------------                                   
def caesar_cipher_logic(text: str, shift: int, mode: str = 'encrypt') -> str:
    """Fungsi untuk enkripsi/dekripsi Caesar Cipher."""
    result = ""
    if mode == 'decrypt':
        shift = -shift
    
    for char in text:
        if 'a' <= char <= 'z':
            new_ord = (ord(char) - ord('a') + shift) % 26
            result += chr(new_ord + ord('a'))
        elif 'A' <= char <= 'Z':
            new_ord = (ord(char) - ord('A') + shift) % 26
            result += chr(new_ord + ord('A'))
        else:
            result += char
    return result

#--------------------------------------------------------
#                   FUNGSI XOR CIPHER
#--------------------------------------------------------   

def xor_cipher(data_bytes: bytes, key: str) -> bytes:
    """Logika inti XOR menggunakan kunci string."""
    key_bytes = key.encode('utf-8')
    # Gunakan itertools.cycle untuk mengulang kunci
    cycled_key = itertools.cycle(key_bytes)
    # Terapkan XOR byte-per-byte
    result_bytes = bytes([b ^ next(cycled_key) for b in data_bytes])
    return result_bytes

def xor_encrypt(plaintext: str, key: str) -> str:
    """Enkripsi teks dengan XOR dan kembalikan sebagai Base64."""
    if not key:
        raise ValueError("Kunci XOR tidak boleh kosong.")
    
    plaintext_bytes = plaintext.encode('utf-8')
    encrypted_bytes = xor_cipher(plaintext_bytes, key)
    # Kembalikan sebagai Base64 agar aman ditampilkan
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def xor_decrypt(ciphertext_b64: str, key: str) -> str:
    """Dekripsi Base64 (dari XOR) kembali ke teks."""
    if not key:
        raise ValueError("Kunci XOR tidak boleh kosong.")
    try:
        # Decode Base64 untuk mendapatkan byte mentah
        ciphertext_bytes = base64.b64decode(ciphertext_b64)
    except binascii.Error:
        raise ValueError("Input dekripsi bukan Base64 yang valid.")
    
    # Proses XOR (identik dengan enkripsi)
    decrypted_bytes = xor_cipher(ciphertext_bytes, key)
    
    try:
        # Coba decode kembali ke string
        return decrypted_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Dekripsi gagal. Kunci salah atau data korup.")
    

#--------------------------------------------------------
#                  FUNGSI Salsa20 CIPHER
#--------------------------------------------------------   
def salsa_encrypt(plaintext_bytes: bytes, password: str) -> bytes | None:
    """
    Enkripsi data menggunakan Salsa20 dengan password.
    Struktur file output: [ 16 byte salt | 8 byte nonce | ...ciphertext... ]
    """
    try:
        # 1. Buat 'salt' acak untuk KDF (Key Derivation Function)
        salt = get_random_bytes(16)
        
        # 2. Hasilkan kunci 32-byte (bytes) menggunakan scrypt.
        #    Pastikan kita menggunakan bytes untuk password saat memanggil scrypt
        password_bytes = password.encode('utf-8')
        key = scrypt(password_bytes, salt, key_len=32, N=2**17, r=8, p=1, num_keys=1)  # type: ignore[arg-type]
        # scrypt may return a tuple when num_keys > 1 in some stubs; normalize to bytes
        if isinstance(key, tuple):
            key = key[0]
        
        # 3. Buat 'nonce' acak (8 byte untuk Salsa20)
        nonce = get_random_bytes(8)
        
        # 4. Buat cipher
        cipher = Salsa20.new(key=key, nonce=nonce)
        
        # 5. Enkripsi data
        ciphertext = cipher.encrypt(plaintext_bytes)
        
        # 6. Kembalikan gabungan [salt] + [nonce] + [ciphertext]
        return salt + nonce + ciphertext
    except (ValueError, KeyError, TypeError) as e:
        print(f"Error Enkripsi Salsa20: {e}")
        return None
def salsa_decrypt(ciphertext_with_meta: bytes, password: str) -> bytes | None:
    """Dekripsi data Salsa20 yang berisi [salt][nonce][ciphertext]"""
    try:
        # 1. Ekstrak meta-data dari file
        salt = ciphertext_with_meta[:16]
        nonce = ciphertext_with_meta[16:24]
        ciphertext = ciphertext_with_meta[24:]
        
        # 2. Hasilkan ulang kunci (key) yang sama menggunakan salt + password
        #    Pastikan kita menggunakan bytes untuk password saat memanggil scrypt
        password_bytes = password.encode('utf-8')
        key = scrypt(password_bytes, salt, key_len=32, N=2**17, r=8, p=1, num_keys=1)  # type: ignore[arg-type]
        if isinstance(key, tuple):
            key = key[0]
        
        # 3. Buat cipher dengan key dan nonce yang diekstrak
        cipher = Salsa20.new(key=key, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext
    except (ValueError, KeyError, TypeError) as e:
        # Gagal jika password salah atau file korup
        print(f"Error Dekripsi Salsa20: {e}")
        return None
# =============================================================================
# === BAGIAN 2: LOGIKA LSB (STEGANOGRAFI GAMBAR) ===
# =============================================================================

# Penanda unik untuk menandai akhir pesan di dalam gambar
DELIMITER = "||--EOF--||"

def text_to_bits(text: str) -> str:
    """Ubah string (misal 'Hi') menjadi string bit ('0100100001101001')"""
    return ''.join(format(ord(char), '08b') for char in text)

def bits_to_text(bits_str: str) -> str:
    """Ubah string bit kembali ke string teks"""
    chars = []
    for i in range(len(bits_str) // 8):
        byte_str = bits_str[i*8:(i+1)*8]
        chars.append(chr(int(byte_str, 2)))
    return "".join(chars)

def lsb_embed(image: Image.Image, secret_text: str) -> Image.Image | None:
    """Sembunyikan teks rahasia ke dalam gambar menggunakan LSB"""
    
    # Tambahkan delimiter ke teks agar kita tahu di mana harus berhenti saat dekripsi
    secret_with_delimiter = secret_text + DELIMITER
    secret_bits = text_to_bits(secret_with_delimiter)
    
    # Konversi gambar ke format NumPy untuk manipulasi cepat
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Hitung kapasitas maksimum
    max_bits = height * width * 3 # 3 channel (RGB)
    if len(secret_bits) > max_bits:
        print("Error: Teks rahasia terlalu besar untuk gambar ini.")
        return None
    
    # 'Flatten' array untuk iterasi mudah
    flat_img = img_array.ravel()
    
    # Tanamkan (embed) bit rahasia ke LSB dari data gambar
    for i in range(len(secret_bits)):
        bit = int(secret_bits[i])
        # & 0xFE memaksa LSB menjadi 0, | bit mengatur LSB ke bit rahasia
        flat_img[i] = (flat_img[i] & 0xFE) | bit
        
    # Bentuk ulang (reshape) array kembali ke dimensi gambar asli
    stego_img_array = flat_img.reshape((height, width, channels))
    
    # Kembalikan sebagai objek Gambar PIL baru
    return Image.fromarray(stego_img_array)

def lsb_extract(image: Image.Image) -> str | None:
    """Ekstrak teks rahasia dari gambar LSB"""
    
    img_array = np.array(image)
    flat_img = img_array.ravel()
    
    extracted_bits = ""
    extracted_text = ""
    
    # Ekstrak LSB bit demi bit
    for pixel_value in flat_img:
        extracted_bits += str(pixel_value & 1) # Ambil LSB
        
        # Jika kita punya cukup bit untuk 1 karakter (8 bit)
        if len(extracted_bits) >= 8:
            byte_str = extracted_bits[:8]
            extracted_bits = extracted_bits[8:] # Hapus bit yang sudah diproses
            
            char = chr(int(byte_str, 2))
            extracted_text += char
            
            # Cek apakah delimiter sudah ditemukan
            if extracted_text.endswith(DELIMITER):
                # Hapus delimiter dari hasil akhir
                return extracted_text[:-len(DELIMITER)]
                
    # Jika loop selesai tanpa menemukan delimiter
    return None