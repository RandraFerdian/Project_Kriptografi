# 🔒 Project_Kriptografi

Sebuah aplikasi **kriptografi & steganografi** berbasis **Python (Streamlit)** yang memungkinkan pengguna untuk melakukan berbagai operasi keamanan data, seperti **enkripsi, dekripsi, serta penyembunyian pesan dalam gambar (steganografi)**.  
Aplikasi ini juga dilengkapi dengan **sistem autentikasi aman menggunakan hashing SHA-3**.

---

## 🧠 Deskripsi Proyek

**Project_Kriptografi** dirancang untuk mempermudah proses pembelajaran dan implementasi konsep kriptografi serta steganografi dalam satu aplikasi terintegrasi.  
Dengan antarmuka berbasis web menggunakan **Streamlit**, pengguna dapat:
- Melakukan **enkripsi dan dekripsi teks** menggunakan berbagai algoritma.
- Menyembunyikan pesan rahasia di dalam gambar (steganografi).
- Mengelola akun dengan keamanan tinggi berkat sistem hashing SHA-3.

---

## 🚀 Fitur Utama

✅ **Autentikasi Pengguna Aman**  
   Menggunakan algoritma hashing **SHA-3** untuk melindungi password pengguna.  

✅ **Kriptografi (Enkripsi & Dekripsi)**  
   - Salsa20  
   - XOR Chiper  
   - Caesar Cipher  
   - LSB  

✅ **Steganografi (Penyembunyian Pesan)**  
   - Menyisipkan pesan ke dalam gambar.  
   - Mengekstrak pesan dari gambar dengan mudah.  

✅ **Antarmuka Web Interaktif**  
   Dibangun menggunakan **Streamlit** dengan tampilan yang sederhana dan mudah digunakan.  

✅ **Struktur Modular & Skalabel**  
   Pemisahan kode dalam direktori `config/`, `model/`, `utils/`, dan `page/` agar mudah dikelola dan dikembangkan.  

---

## 🧩 Teknologi yang Digunakan

| Komponen | Teknologi |
|-----------|------------|
| Bahasa Pemrograman | Python 3.x |
| Framework UI | Streamlit |
| Kriptografi | Library `cryptography` |
| Hashing | SHA-3 |
| Basis Data | MySQL (`kriptografi.sql`) |
| Manajemen Dependensi | `requirements.txt` |

---
