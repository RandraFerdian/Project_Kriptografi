import streamlit as st
from streamlit_option_menu import option_menu

# Impor fungsi halaman Anda
from page.page_login import show_login_page
from page.page_register import show_register_page
from page.page_dashboard import show_dashboard_page 
from page.page_history import show_history_page
from page.page_super_encryption import show_super_encryption_page
from page.page_upload import show_upload_page
# (Anda bisa tambahkan page_upload, page_history, dll)

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Aplikasi Kriptografi",
    page_icon="🔒",
    layout="centered", # 'wide' atau 'centered'
    initial_sidebar_state="collapsed" # Sembunyikan sidebar
)

# --- Sembunyikan Dekorasi Streamlit (Termasuk tombol menu) ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# --- Inisialisasi Session State ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['user_id'] = None

# --- Logika Navigasi ---
# Tampilkan menu yang berbeda berdasarkan status login

if not st.session_state['logged_in']:
    # --- MENU UNTUK USER YANG BELUM LOGIN ---
    selected = option_menu(
        menu_title=None,  # Wajib ada, tapi bisa dikosongkan
        options=["Login", "Sign In (Register)"],  # Pilihan menu
        icons=["box-arrow-in-right", "person-plus"],  # Ikon (opsional)
        menu_icon="cast",  # Ikon menu (opsional)
        default_index=0,
        orientation="horizontal", # INI KUNCINYA!
    )
    
    # Tampilkan halaman berdasarkan pilihan menu
    if selected == "Login":
        show_login_page()
    elif selected == "Sign In (Register)":
        show_register_page()

else:
    # --- MENU UNTUK USER YANG SUDAH LOGIN ---
    selected = option_menu(
        menu_title=f"Halo, {st.session_state['username']}!", # Sapa user
        options=["Dashboard", "Upload File","Teks Super Encryption" ,"History", "Logout"], # Menu setelah login
        icons=["house", "cloud-upload","pencil" ,"clock-history", "box-arrow-right"],
        menu_icon="person-circle",
        default_index=0,
        orientation="horizontal",
    )

    # Tampilkan halaman berdasarkan pilihan menu
    if selected == "Dashboard":
        show_dashboard_page()
    elif selected == "Upload File":
        # Panggil fungsi dari modul 'page_upload.py' Anda
        st.title("Halaman Upload") 
        show_upload_page()
    elif selected == "Teks Super Encryption":
        show_super_encryption_page()
    elif selected == "History":
        show_history_page()
        # (Logika untuk mengambil data dari 'history' berdasarkan user_id)
    elif selected == "Logout":
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['user_id'] = None
        st.success("Anda berhasil logout.")
        st.rerun()