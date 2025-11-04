import streamlit as st
# --- IMPORT FUNGSI DARI UTILS ---
from utils.encryption import (
    caesar_cipher_logic,
    xor_encrypt,
    xor_decrypt
)
from model.model_histori import add_history_entry

def show_super_encryption_page():
    st.title("🛡️ Super Encryption (Caesar + XOR)")
    st.image("https://img.icons8.com/color/96/data-encryption.png", width=80)
    st.write(
        "Ini adalah metode **Enkripsi Berlapis (Chaining)**. "
        "Pesan Anda akan dienkripsi dua kali: pertama dengan **Caesar Cipher**, "
        "lalu hasilnya dienkripsi lagi dengan **XOR Cipher**."
    )
    st.warning(
        "**Penting:** Untuk dekripsi, Anda harus memasukkan **kedua kunci** "
        "(Caesar Shift dan Kunci XOR) dengan benar."
    )
    
    user_id = st.session_state.get('user_id')
    
    st.divider()

    # --- 1. BAGIAN ENKRIPSI ---
    st.header("1. Enkripsi")
    with st.form("super_encrypt_form"):
        st.write("Masukkan pesan dan dua kunci (Caesar & XOR).")
        
        message_to_encrypt = st.text_area("Pesan yang Ingin Dienkripsi:")
        
        col1, col2 = st.columns(2)
        with col1:
            caesar_shift = st.slider(
                "Kunci 1: Caesar Shift", 
                min_value=1, 
                max_value=25, 
                value=7,
                help="Kunci numerik (1-25) untuk lapisan pertama."
            )
        with col2:
            xor_key = st.text_input(
                "Kunci 2: Kunci XOR", 
                type="password",
                help="Kunci teks rahasia (misal: 'rahasia123') untuk lapisan kedua."
            )
        
        encrypt_button = st.form_submit_button("Enkripsi Sekarang")

    if encrypt_button:
        if not message_to_encrypt:
            st.warning("Silakan masukkan pesan.")
        elif not xor_key:
            st.warning("Silakan masukkan Kunci XOR.")
        elif not user_id:
            st.error("Sesi tidak ditemukan. Tidak dapat menyimpan histori.")
        else:
            try:
                # --- Proses Enkripsi Berlapis ---
                # 1. Enkripsi dengan Caesar
                caesar_result = caesar_cipher_logic(
                    message_to_encrypt, 
                    caesar_shift, 
                    'encrypt'
                )
                
                # 2. Enkripsi hasil Caesar dengan XOR
                final_result = xor_encrypt(caesar_result, xor_key)
                
                st.subheader("🎉 Enkripsi Berhasil!")
                st.write("Data Anda telah dienkripsi dengan Caesar + XOR:")
                st.text_area("Hasil Super Enkripsi (Base64)", final_result, height=100)
                
                # Simpan ke session untuk demo dekripsi
                st.session_state['super_ciphertext'] = final_result
                
                add_history_entry(
                    user_id=user_id,
                    data_type="text", # Harus "text", "image", atau "file"
                    original_data=message_to_encrypt,
                    encrypted_data=final_result
                )
                st.toast("Tersimpan ke riwayat!")
            
            except Exception as e:
                st.error(f"Terjadi kesalahan saat enkripsi: {e}")

    st.divider()

    # --- 2. BAGIAN DEKRIPSI ---
    st.header("2. Dekripsi")
    with st.form("super_decrypt_form"):
        st.write(
            "Masukkan ciphertext (Base64) dan **kedua kunci** "
            "yang sama persis untuk dekripsi."
        )
        
        # Ambil dari session state jika ada (untuk demo)
        default_ciphertext = st.session_state.get('super_ciphertext', "")
        
        ciphertext_input = st.text_area(
            "Ciphertext (Base64)", 
            value=default_ciphertext,
            height=100
        )
        
        col_dec_1, col_dec_2 = st.columns(2)
        with col_dec_1:
            caesar_shift_dec = st.slider(
                "Kunci 1: Caesar Shift", 
                min_value=1, 
                max_value=25, 
                value=7,
                key="caesar_dec"
            )
        with col_dec_2:
            xor_key_dec = st.text_input(
                "Kunci 2: Kunci XOR", 
                type="password",
                key="xor_dec"
            )

        decrypt_button = st.form_submit_button("Dekripsi Sekarang")

    if decrypt_button:
        if not ciphertext_input:
            st.warning("Silakan masukkan ciphertext.")
        elif not xor_key_dec:
            st.warning("Silakan masukkan Kunci XOR.")
        elif not user_id:
            st.error("Sesi tidak ditemukan. Tidak dapat menyimpan histori.")
        else:
            try:
                # --- Proses Dekripsi Berlapis (Urutan terbalik) ---
                
                # 1. Dekripsi dengan XOR
                xor_result = xor_decrypt(ciphertext_input, xor_key_dec)
                
                # 2. Dekripsi hasil XOR dengan Caesar
                final_result = caesar_cipher_logic(
                    xor_result, 
                    caesar_shift_dec, 
                    'decrypt'
                )
                
                st.subheader("✅ Dekripsi Berhasil!")
                st.success(f"Pesan Asli: **{final_result}**")
                
                add_history_entry(
                    user_id=user_id,
                    data_type="text", # Harus "text", "image", atau "file"
                    original_data=message_to_encrypt,
                    encrypted_data=final_result
                )
                st.toast("Tersimpan ke riwayat!")

            except ValueError as e:
                st.error(f"Dekripsi gagal. Pastikan Kunci XOR dan format Base64 benar. Error: {e}")
            except Exception as e:
                st.error(f"Terjadi kesalahan tak terduga: {e}")