import streamlit as st

# Konfigurasi halaman harus menjadi perintah Streamlit pertama
st.set_page_config(
    page_title="Aplikasi Laporan Prodsus",
    page_icon="📊",
    layout="wide"
)

from datetime import datetime
import os
import sqlite3
from sqlite3 import Error
import sys

# Fungsi untuk format mata uang Rupiah
def format_currency(value):
    # Konversi input string ke float jika mengandung titik
    if isinstance(value, str):
        value = float(value.replace('.', '')) if '.' in value else float(value)
    return f"Rp {value:,.0f}".replace(',', '.')

# Fungsi untuk menghitung total dan achievement
def hitung_spd_ach(target_bulanan, target_shift2, akm_sales):
    total_target = target_bulanan if target_bulanan else 0
    if total_target == 0:
        return total_target, "", ""
    
    # Hitung SPD (Akumulasi sales dibagi tanggal berikutnya)
    spd = akm_sales / (datetime.now().day + 1) if akm_sales else 0
    
    # Hitung ACH (SPD dibagi target x 100)
    ach = (spd / total_target) * 100 if total_target > 0 else 0
    
    return total_target, format_currency(spd), f"{ach:.2f}%"

# Fungsi utama
def main():
    st.title("Aplikasi Laporan Prodsus")
    
    # Input tanggal dan nama toko
    tanggal = st.date_input("Tanggal Laporan", datetime.now())
    nama_toko = st.text_input("Nama Toko", "TCBS")
    
    # Daftar produk
    produk_list = [
        "Saybread", "Sosis", "Buah lokal", "Buah Import", 
        "Kue Basah", "Mr bread", "Telur", "Other bakery"
    ]
    
    # Dictionary untuk menyimpan data target bulanan
    target_bulanan = {}
    
    # Input target bulanan untuk setiap produk
    st.subheader("Input Target Bulanan")
    for produk in produk_list:
        target_bulanan[produk] = st.number_input(f"Target Bulanan ({produk})", key=f"target_{produk}", format="%.0f", value=0.0)
    
    # Dictionary untuk menyimpan data harian
    data_produk = {}
    
    # Input data harian untuk setiap produk
    st.subheader("Input Penjualan Harian")
    for produk in produk_list:
        st.subheader(f"*{produk}*")
        
        col1, col2 = st.columns(2)
        with col1:
            penjualan_shift1 = st.number_input(f"Penjualan Shift 1 ({produk})", key=f"shift1_{produk}", format="%.0f", value=0.0)
        with col2:
            penjualan_shift2 = st.number_input(f"Penjualan Shift 2 ({produk})", key=f"shift2_{produk}", format="%.0f", value=0.0)
        
        # Hitung total penjualan harian
        total_penjualan = penjualan_shift1 + penjualan_shift2
        
        # Hitung SPD dan ACH
        total, spd, ach = hitung_spd_ach(target_bulanan[produk], 0, total_penjualan)
        
        data_produk[produk] = {
            "target_bulanan": target_bulanan[produk],
            "penjualan_shift1": penjualan_shift1,
            "penjualan_shift2": penjualan_shift2,
            "total": total_penjualan,
            "akm_sales": total_penjualan,
            "spd": spd,
            "ach": ach
        }
    
    # Tombol simpan data
    if st.button("Simpan Data"):
        try:
            # Buat koneksi ke database SQLite
            conn = sqlite3.connect('prodsus_database.db')
            cursor = conn.cursor()
            
            # Buat tabel jika belum ada
            cursor.execute('''CREATE TABLE IF NOT EXISTS prodsus_data
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             tanggal TEXT,
                             nama_toko TEXT,
                             produk TEXT,
                             target_bulanan REAL,
                             penjualan_shift1 REAL,
                             penjualan_shift2 REAL,
                             total REAL,
                             akm_sales REAL,
                             spd TEXT,
                             ach TEXT)''')
            
            # Simpan data untuk setiap produk
            for produk, data in data_produk.items():
                cursor.execute('''INSERT INTO prodsus_data 
                                (tanggal, nama_toko, produk, target_bulanan, 
                                penjualan_shift1, penjualan_shift2, total, 
                                akm_sales, spd, ach)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                (tanggal.strftime('%Y-%m-%d'), nama_toko, produk,
                                data['target_bulanan'], data['penjualan_shift1'],
                                data['penjualan_shift2'], data['total'],
                                data['akm_sales'], data['spd'], data['ach']))
            
            conn.commit()
            st.session_state.target_bulanan = target_bulanan
            st.session_state.data_produk = data_produk
            st.success("Data berhasil disimpan ke database!")
        except Error as e:
            st.error(f"Terjadi error saat menyimpan data: {e}")
        finally:
            if conn:
                conn.close()
        
    # Tombol generate laporan
    if st.button("Generate Laporan"):
        # Format laporan
        laporan = f"Laporan insentive prodsus *{nama_toko}*\n"
        laporan += f"Tgl {tanggal.strftime('%d %B %Y')}\n\n"
        
        for produk, data in data_produk.items():
            laporan += f"*{produk}*\n"
            laporan += "Target :\n"
            laporan += f"Bulanan : {format_currency(data['target_bulanan'])}\n"
            laporan += f"Shift1  : {format_currency(data['penjualan_shift1'])}\n"
            laporan += f"Shift2 : {format_currency(data['penjualan_shift2'])}\n"
            laporan += f"Total : {format_currency(data['total'])}\n"
            laporan += f"Akm sales : {format_currency(data['akm_sales'])}\n"
            laporan += f"SPD : {data['spd']}\n"
            laporan += f"ACH : {data['ach']}\n\n"
        
        # Simpan ke file
        with open("Prodsus.txt", "w") as f:
            f.write(laporan)
        
        st.success("Laporan berhasil dibuat dan disimpan di Prodsus.txt")
        st.download_button("Download Laporan", laporan, "Prodsus.txt")

def show_prodsus_report():
    main()

# Fungsi untuk menampilkan menu navigasi
def show_navigation():
    # Import sys di dalam fungsi untuk menghindari UnboundLocalError
    import sys
    # Tambahkan path ke direktori yang berisi app_sqlite.py di awal
    sqlite_path = os.path.join(os.path.dirname(__file__), 'aplikasi_laporan_penjualan_sqlite-1')
    
    # Pastikan path ada di sys.path dan tambahkan di awal list
    if sqlite_path in sys.path:
        sys.path.remove(sqlite_path)
    sys.path.insert(0, sqlite_path)
    
    st.sidebar.title('Menu Aplikasi')
    app_choice = st.sidebar.radio(
        'Pilih Aplikasi:',
        ('Laporan Penjualan', 'Laporan Prodsus')
    )
    
    if app_choice == 'Laporan Penjualan':
        try:
            # Import dan jalankan aplikasi laporan penjualan
            import importlib.util
            import sys
            
            # Cari file app_sqlite.py secara eksplisit
            app_sqlite_path = os.path.join(sqlite_path, 'app_sqlite.py')
            
            if os.path.exists(app_sqlite_path):
                # Gunakan importlib untuk memuat modul secara dinamis
                spec = importlib.util.spec_from_file_location("app_sqlite", app_sqlite_path)
                app_sqlite = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(app_sqlite)
                
                # Jalankan fungsi main dari modul yang dimuat
                app_sqlite.main()
            else:
                st.error(f"File app_sqlite.py tidak ditemukan di: {app_sqlite_path}")
        except Exception as e:
            st.error(f"Error saat memuat aplikasi laporan penjualan: {e}")
            st.code(f"Path yang dicoba: {sqlite_path}")
            st.code(f"sys.path: {sys.path}")
    elif app_choice == 'Laporan Prodsus':
        show_prodsus_report()

if __name__ == "__main__":
    show_navigation()