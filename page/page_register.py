import streamlit as st
from model.model_user import create_user

def show_register_page():
    st.title("📝 Halaman Registrasi")

    with st.form(key='register_form'):
        username = st.text_input("Username Baru")
        password = st.text_input("Password Baru", type="password")
        confirm_password = st.text_input("Konfirmasi Password", type="password")
        submit_button = st.form_submit_button(label="Daftar")

    if submit_button:
        if not username or not password or not confirm_password:
            st.warning("Semua kolom harus diisi.")
        elif password != confirm_password:
            st.error("Password dan Konfirmasi Password tidak cocok.")
        else:
            success = create_user(username, password)
            if success:
                st.success("Registrasi berhasil! Silakan login.")
            else:
                st.error("Registrasi gagal. Username mungkin sudah digunakan.")