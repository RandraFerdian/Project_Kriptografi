import streamlit as st
import sys
import os
from model.model_user import check_user_login

def show_login_page():
    st.title("🔐 Halaman Login")

    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Login")

    if submit_button:
        if not username or not password:
            st.warning("Username dan Password tidak boleh kosong.")
        else:
            login_success, user_id = check_user_login(username, password)
            
            if login_success:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['user_id'] = user_id
                st.success("Login Berhasil!")
                st.rerun() # Muat ulang halaman untuk menampilkan menu baru
            else:
                st.error("Username atau Password salah.")