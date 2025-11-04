import streamlit as st
from PIL import Image
import io

# --- Impor fungsi logika kita ---
from utils.encryption import (
    salsa_encrypt, salsa_decrypt,
    lsb_embed, lsb_extract
)

def show_upload_page():
    st.title("☁️ Upload & Enkripsi File")
    st.write("Pilih metode keamanan Anda: Steganografi untuk gambar atau Enkripsi untuk file.")
    
    # --- BUAT DUA TAB UTAMA ---
    tab_stego, tab_salsa = st.tabs([
        "Steganografi Gambar (Sembunyikan Teks)", 
        "Enkripsi File (Salsa20)"
    ])

    # =========================================================================
    # === TAB 1: STEGANOGRAFI (LSB) ===
    # =========================================================================
    with tab_stego:
        st.header("Sembunyikan Teks di dalam Gambar")
        st.info("Metode ini menggunakan **Steganografi LSB (Least Significant Bit)** untuk menanamkan teks rahasia ke dalam gambar PNG tanpa mengubah tampilannya secara kasat mata.")
        
        # Buat sub-tab untuk Enkripsi dan Dekripsi
        sub_tab_stego_enc, sub_tab_stego_dec = st.tabs(["Sembunyikan Teks", "Ekstrak Teks"])
        
        # --- Steganografi -> Sembunyikan Teks ---
        with sub_tab_stego_enc:
            st.subheader("Sembunyikan Teks")
            uploader_img_enc = st.file_uploader(
                "1. Unggah Gambar", 
                type=["png","jpg","jpeg"], 
                key="stego_img_enc"
            )
            secret_text = st.text_area("2. Masukkan Teks Rahasia Anda:")
            
            if st.button("Sembunyikan Teks", key="stego_enc_btn"):
                if uploader_img_enc and secret_text:
                    try:
                        # Baca gambar menggunakan PIL
                        image = Image.open(io.BytesIO(uploader_img_enc.read()))
                        
                        # Panggil logika LSB
                        stego_image = lsb_embed(image, secret_text)
                        
                        if stego_image is None:
                            st.error("Enkripsi Gagal: Teks rahasia terlalu besar untuk gambar ini.")
                        else:
                            # Konversi hasil gambar ke bytes untuk diunduh
                            buf = io.BytesIO()
                            stego_image.save(buf, format="PNG")
                            img_bytes = buf.getvalue()
                            
                            st.success("Teks berhasil disembunyikan!")
                            st.download_button(
                                "Unduh Gambar Baru (.png)",
                                data=img_bytes,
                                file_name="gambar_tersembunyi.png",
                                mime="image/png"
                            )
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")
                else:
                    st.warning("Harap unggah gambar dan masukkan teks rahasia.")

        # --- Steganografi -> Ekstrak Teks ---
        with sub_tab_stego_dec:
            st.subheader("Ekstrak Teks")
            uploader_img_dec = st.file_uploader(
                "1. Unggah Gambar (.png) yang berisi rahasia", 
                type=["png"], 
                key="stego_img_dec"
            )
            
            if st.button("Ekstrak Teks", key="stego_dec_btn"):
                if uploader_img_dec:
                    try:
                        # Baca gambar
                        image = Image.open(io.BytesIO(uploader_img_dec.read()))
                        
                        # Panggil logika LSB
                        extracted_text = lsb_extract(image)
                        
                        if extracted_text is None:
                            st.error("Tidak ada teks rahasia yang ditemukan di dalam gambar ini.")
                        else:
                            st.success("Teks rahasia berhasil diekstrak:")
                            st.code(extracted_text, language=None)
                            
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")
                else:
                    st.warning("Harap unggah gambar.")

    # =========================================================================
    # === TAB 2: ENKRIPSI FILE (SALSA20) ===
    # =========================================================================
    with tab_salsa:
        st.header("Enkripsi File dengan Salsa20")
        st.info("Metode ini menggunakan **Salsa20**, algoritma stream cipher yang cepat dan aman. Seluruh isi file akan dienkripsi menggunakan password Anda.")
        
        # Buat sub-tab untuk Enkripsi dan Dekripsi
        sub_tab_salsa_enc, sub_tab_salsa_dec = st.tabs(["Enkripsi File", "Dekripsi File"])

        # --- Salsa20 -> Enkripsi ---
        with sub_tab_salsa_enc:
            st.subheader("Enkripsi File")
            uploader_file_enc = st.file_uploader(
                "1. Unggah File (Ukuran Apapun)", 
                key="salsa_file_enc"
            )
            password_enc = st.text_input(
                "2. Masukkan Password", 
                type="password", 
                key="salsa_pass_enc"
            )
            
            if st.button("Enkripsi File", key="salsa_enc_btn"):
                if uploader_file_enc and password_enc:
                    try:
                        file_bytes = uploader_file_enc.read()
                        
                        # Panggil logika Salsa20
                        encrypted_bytes = salsa_encrypt(file_bytes, password_enc)
                        
                        if encrypted_bytes:
                            st.success("File berhasil dienkripsi!")
                            st.download_button(
                                "Unduh File Terenkripsi (.enc)",
                                data=encrypted_bytes,
                                file_name=uploader_file_enc.name + ".enc",
                                mime="application/octet-stream"
                            )
                        else:
                            st.error("Enkripsi gagal.")
                            
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")
                else:
                    st.warning("Harap unggah file dan masukkan password.")

        # --- Salsa20 -> Dekripsi ---
        with sub_tab_salsa_dec:
            st.subheader("Dekripsi File")
            uploader_file_dec = st.file_uploader(
                "1. Unggah File Terenkripsi (.enc)", 
                type=None, 
                key="salsa_file_dec",
                accept_multiple_files=False
            )
            password_dec = st.text_input(
                "2. Masukkan Password", 
                type="password", 
                key="salsa_pass_dec"
            )
            
            if st.button("Dekripsi File", key="salsa_dec_btn"):
                if uploader_file_dec and password_dec:
                    try:
                        file_bytes = uploader_file_dec.read()
                        
                        # Panggil logika Salsa20
                        decrypted_bytes = salsa_decrypt(file_bytes, password_dec)
                        
                        if decrypted_bytes is None:
                            st.error("Dekripsi Gagal! Password salah atau file korup.")
                        else:
                            st.success("File berhasil didekripsi!")
                            # Coba tebak nama file asli
                            original_name = uploader_file_dec.name.replace(".enc", "")
                            if not original_name: 
                                original_name = "file_didekripsi"
                                
                            st.download_button(
                                "Unduh File Asli",
                                data=decrypted_bytes,
                                file_name=original_name,
                                mime="application/octet-stream"
                            )
                            
                    except Exception as e:
                        st.error(f"Dekripsi Gagal! Kemungkinan password salah. Error: {e}")
                else:
                    st.warning("Harap unggah file (.enc) dan masukkan password.")
