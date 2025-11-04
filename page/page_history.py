import streamlit as st
from model.model_histori import get_history_by_user, delete_history_entry

def show_history_page():
    st.title("🕒 Riwayat Aktivitas")

    # 1. Cek Status Login
    if not st.session_state.get('logged_in', False):
        st.error("Anda harus login untuk melihat riwayat.")
        st.page_link("page/page_login.py", label="Pergi ke Halaman Login", icon="🔐")
        return

    # 2. Dapatkan user_id dari sesi
    user_id = st.session_state.get('user_id')
    if not user_id:
        st.error("Sesi Anda tidak valid. Silakan login kembali.")
        return

    # 3. Ambil Data dari Model
    history_records = get_history_by_user(user_id)

    # 4. Tampilkan Data
    if not history_records:
        st.info("Anda belum memiliki riwayat aktivitas.")
        st.write("Coba enkripsi sesuatu di halaman 'Super Encryption' dan data akan muncul di sini.")
        return

    st.write(f"Menampilkan **{len(history_records)}** riwayat terakhir Anda.")

    # 5. Iterasi dan Tampilkan setiap entri
    for record in history_records:
        # Gunakan st.expander untuk setiap entri agar rapi
        # Format 'created_at' agar lebih mudah dibaca
        date_time = record['created_at'].strftime("%d %B %Y, %H:%M:%S")
        
        with st.expander(f"**{record['data_type'].capitalize()}** - {date_time}"):
            
            st.subheader("Data Asli (Plaintext)")
            st.code(record['original_data'], language=None)
            
            st.subheader("Data Terenkripsi (Ciphertext)")
            st.text_area(
                "Ciphertext", 
                value=record['encrypted_data'], 
                height=100, 
                disabled=True,
                key=f"enc_{record['id']}" # Kunci unik untuk widget
            )
            
            st.write("") # Memberi spasi
            
            # Tombol Hapus (opsional tapi sangat direkomendasikan)
            if st.button("Hapus Riwayat Ini", key=f"del_{record['id']}", type="secondary"):
                success = delete_history_entry(record['id'], user_id)
                if success:
                    st.success("Riwayat berhasil dihapus.")
                    st.rerun() # Muat ulang halaman untuk update
                else:
                    st.error("Gagal menghapus riwayat.")