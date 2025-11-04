import streamlit as st


def show_dashboard_page():
    
    # 1. Judul dan Sambutan
    st.title(f"Selamat Datang, {st.session_state.get('username', 'Pengguna')}! 👋")
    st.write(
        "Ini adalah **dashboard utama aplikasi kriptografi Anda.** "
        "Gunakan menu navigasi di atas untuk menjelajahi fitur-fitur kami yang aman."
    )
    st.divider()

    # 2. Layout Kolom
    col1, col2 = st.columns(2)

    # --- Kartu Fitur 1: Upload File ---
    with col1:
        with st.container(border=True): # Gunakan container dengan border untuk efek kartu
            st.markdown("### ☁️ Upload File") # Subheader lebih besar
            st.write(
                "Unggah file **(gambar, teks, dokumen)** Anda untuk dienkripsi atau didekripsi dengan aman."
                " File Anda akan diproses dan disimpan dalam riwayat aktivitas Anda."
            )
            st.info("💡 **Pilih 'Upload File' dari menu navigasi di atas** untuk memulai.") # Pesan instruktif

    # --- Kartu Fitur 2: Super Encryption ---
    with col2:
        with st.container(border=True):
            st.markdown("### 🛡️ Super Encryption") # Subheader lebih besar
            st.write(
                "Enkripsi teks sensitif Anda menggunakan **metode berlapis (Caesar + XOR)** kami."
                " Dapatkan hasil enkripsi instan dan jaga kerahasiaan pesan Anda."
            )
            st.info("💡 **Pilih 'Super Encryption' dari menu navigasi di atas** untuk mencoba.") # Pesan instruktif

    st.divider() # Pemisah antar baris kartu

    # --- Kartu Fitur 3: History ---
    with st.container(border=True):
        st.markdown("### 🕒 History") # Subheader lebih besar
        st.write(
            "Lihat semua **riwayat aktivitas enkripsi dan dekripsi** yang pernah Anda lakukan."
            " Semua data tersimpan aman dan terhubung dengan akun Anda, mudah diakses kapan saja."
        )
        st.info("💡 **Pilih 'History' dari menu navigasi di atas** untuk melihat riwayat lengkap Anda.") # Pesan instruktif